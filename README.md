# 📰 Sistem Rekomendasi Berita

Sistem rekomendasi berita berbasis AI menggunakan **vector embedding** dan **KNN similarity search** untuk memberikan rekomendasi artikel yang personal kepada setiap pengguna.

## 🛠️ Tech Stack

- **FastAPI** - Web framework untuk REST API
- **Manticore Search** - Vector database dengan auto-embedding dan KNN search
- **MySQL** - Database untuk menyimpan artikel dan riwayat baca user
- **SQLModel** - ORM untuk interaksi dengan MySQL
- **NumPy** - Komputasi numerik untuk operasi vektor

---

## 📋 Prasyarat

- Python 3.12+
- pip (Python package manager)
- **Pilihan 1:** Docker & Docker Compose (recommended untuk setup cepat)
- **Pilihan 2:** MySQL 8.0+ dan Manticore Search 6.0+ (instalasi manual)

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd recommendation
```

### 2. Setup Environment Variables

Salin file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Edit `.env` sesuai kebutuhan:

```env
# Database MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_ROOT_PASSWORD=password
DB_NAME=rec

# Manticore Search
MANTICORE_HOST=localhost
MANTICORE_PORT=9308
```

### 3. Install Dependencies

```bash
# Buat virtual environment
python -m venv .venv

# Aktifkan virtual environment
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

### 4. Setup Database & Services

Anda bisa pilih salah satu dari 2 opsi berikut:

#### **Opsi A: Menggunakan Docker (Recommended)** 🐳

```bash
# Jalankan MySQL dan Manticore menggunakan Docker
docker-compose up -d
```

Ini akan menjalankan:
- MySQL di port `3306`
- Manticore Search di port `9308` (HTTP) dan `9306` (SQL)

#### **Opsi B: Instalasi Manual (Tanpa Docker)** 💻

**Install MySQL:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Set password untuk root user
sudo mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> FLUSH PRIVILEGES;
mysql> exit;

# Buat database
mysql -u root -ppassword -e "CREATE DATABASE IF NOT EXISTS rec;"
```

```bash
# macOS (menggunakan Homebrew)
brew install mysql
brew services start mysql

# Set password dan buat database
mysql -u root
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
mysql> CREATE DATABASE IF NOT EXISTS rec;
mysql> exit;
```

**Install Manticore Search:**

```bash
# Ubuntu/Debian
wget https://repo.manticoresearch.com/manticore-repo.noarch.deb
sudo dpkg -i manticore-repo.noarch.deb
sudo apt update
sudo apt install manticore manticore-extra

# Start Manticore
sudo systemctl start manticore
sudo systemctl enable manticore
```

```bash
# macOS (menggunakan Homebrew)
brew install manticoresearch

# Start Manticore
brew services start manticoresearch
# atau jalankan di foreground:
searchd --config /opt/homebrew/etc/manticoresearch/manticore.conf
```

**Catatan untuk Windows:**
- Gunakan Docker Desktop atau WSL2 dengan instruksi Linux di atas
- Atau download binary Manticore dari [official website](https://manticoresearch.com/install/)

### 5. Import Database Schema

**Untuk Docker:**
```bash
# Import schema MySQL
mysql -h localhost -u root -ppassword rec < migrations/001_init_mysql.sql

# Setup Manticore index dengan auto-embedding
mysql -h 127.0.0.1 -P 9306 < migrations/002_init_manticore.sql
```

**Untuk Instalasi Manual:**
```bash
# Import schema MySQL
mysql -u root -ppassword rec < migrations/001_init_mysql.sql

# Setup Manticore index
# Pastikan searchd sedang berjalan terlebih dahulu
mysql -h 127.0.0.1 -P 9306 < migrations/002_init_manticore.sql
```

### 6. Jalankan Aplikasi

```bash
fastapi dev app/main.py
```

Aplikasi akan berjalan di: **http://localhost:8000**

---

## 🔄 Cara Kerja Sistem Rekomendasi

Sistem ini menggunakan **4 tahap** untuk menghasilkan rekomendasi personal:

### **TAHAP 1: Inisialisasi**

```
┌─────────────────┐
│ Data Berita     │
│ (MySQL)         │
└────────┬────────┘
         │
         │ Sync & Auto-Embedding
         ▼
┌─────────────────┐
│ Manticore       │
│ (Vector Store)  │
│                 │
│ Model: sentence-│
│ transformers    │
└─────────────────┘
```

- Data berita dipindahkan dari MySQL ke Manticore
- Manticore otomatis membuat **embedding vector** dari artikel menggunakan model `sentence-transformers`
- Setiap artikel direpresentasikan sebagai vector berdimensi tinggi

**Riwayat baca user** disimpan di MySQL untuk tracking.

---

### **TAHAP 2: User Profiling (User Interest Vector)**

```
User History → [Article 1, Article 2, Article 3]
                    ↓           ↓           ↓
             Vector 1    Vector 2    Vector 3
                    ↓           ↓           ↓
                    └───────────┴───────────┘
                              │
                     Calculate Average
                              ↓
                        User Vector
                    (Titik Minat User)
```

**Proses:**
1. Ambil riwayat artikel yang pernah dibaca user dari MySQL
2. Ambil **embedding vector** dari setiap artikel tersebut dari Manticore
3. Hitung **rata-rata (mean)** dari semua vector
4. Hasil rata-rata = **User Vector** (representasi minat user)

**Contoh:**
```python
# User membaca 3 artikel dengan vector:
vec1 = [0.5, 0.2, -0.3]
vec2 = [0.4, 0.3, -0.2]
vec3 = [0.6, 0.1, -0.4]

# User vector = rata-rata
user_vec = [0.5, 0.2, -0.3]  # Titik tengah minat user
```

---

### **TAHAP 3: Similarity Scoring (KNN Search)**

```
User Vector → Manticore KNN Search
                    ↓
      ┌─────────────────────────────┐
      │ Article 1 (distance: 0.12)  │
      │ Article 2 (distance: 0.18)  │
      │ Article 3 (distance: 0.25)  │
      │ Article 4 (distance: 0.30)  │
      │          ...                │
      └─────────────────────────────┘
```

**Proses:**
- Gunakan **KNN (K-Nearest Neighbors)** search di Manticore
- Cari artikel dengan vector yang **paling mirip** dengan user vector
- Manticore mengembalikan artikel beserta **knn_distance** (similarity score)
- **Semakin kecil distance, semakin relevan** artikel tersebut

**Query Example:**
```sql
SELECT id, article_id, knn_distance 
FROM articles 
WHERE knn(embedding_vector, 20, (0.5, 0.2, -0.3, ...))
ORDER BY knn_distance 
LIMIT 20
```

**Output:**
```json
[
  {"id": 1, "article_id": 101, "knn_distance": 0.12},
  {"id": 2, "article_id": 102, "knn_distance": 0.18},
  ...
]
```

---

### **TAHAP 4: Ranking & Filtering**

```
Similarity Results
        ↓
    Filtering
        ↓
┌───────────────────────────┐
│ ❌ Artikel > 3 hari lalu  │ → HAPUS
│ ❌ Sudah dibaca user      │ → HAPUS
│ ✅ Fresh & Belum dibaca   │ → KEEP
└───────────────────────────┘
        ↓
   Sort by Score
        ↓
   Top 10 Articles
```

**Aturan Filtering:**

| Kondisi | Aksi |
|---------|------|
| Artikel > 3 hari lalu | ❌ **Hapus** dari list |
| Artikel sudah dibaca user | ❌ **Hapus** dari list |
| Artikel fresh & belum dibaca | ✅ **Tetap** di list |

**Proses:**
1. Ambil artikel dari tahap 3 dengan score paling rendah (paling relevan)
2. Filter artikel yang sudah kadaluarsa (> 3 hari)
3. Filter artikel yang sudah pernah dibaca user
4. Urutkan berdasarkan `knn_distance` (ascending)
5. Ambil **top 10** artikel
6. Return sebagai rekomendasi final

---

## 🌐 API Endpoints

### **1. Get Recommendation**

Dapatkan rekomendasi artikel untuk user tertentu.

```http
GET /api/recommendation/{user_id}?limit={limit}
```

**Parameters:**
- `user_id` (path) - ID user
- `limit` (query, optional) - Jumlah rekomendasi (default: 10)

**Response:**
```json
{
  "user_id": 1,
  "recommendations": [
    {
      "article_id": 101,
      "title": "Breaking News: AI Revolution",
      "category": "Technology",
      "score": 0.12,
      "published_at": "2026-02-10T10:00:00"
    }
  ],
  "total": 10
}
```

**Example:**
```bash
curl http://localhost:8000/api/recommendation/1?limit=10
```

---

### **2. Search News (Semantic Search)**

Cari berita menggunakan pencarian semantik.

```http
GET /api/news?q={keyword}&limit={limit}
```

**Parameters:**
- `q` (query) - Kata kunci pencarian
- `limit` (query, optional) - Jumlah hasil (default: 10)

**Response:**
```json
{
  "query": "teknologi AI",
  "results": [
    {
      "article_id": 102,
      "title": "Perkembangan AI di Indonesia",
      "similarity_score": 0.85
    }
  ],
  "total": 5
}
```

**Example:**
```bash
curl "http://localhost:8000/api/news?q=teknologi%20AI&limit=5"
```

---

### **3. Insert News**

Tambah artikel baru ke Manticore.

```http
POST /api/news
```

**Request Body:**
```json
{
  "article_id": 103,
  "title": "Judul Berita",
  "content": "Isi berita lengkap...",
  "category": "Technology"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Article inserted successfully",
  "article_id": 103
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/news \
  -H "Content-Type: application/json" \
  -d '{
    "article_id": 103,
    "title": "Test Article",
    "content": "This is a test article content"
  }'
```

---

### **4. Update News**

Update artikel yang sudah ada di Manticore.

```http
PUT /api/news/{news_id}
```

**Request Body:**
```json
{
  "title": "Judul Baru",
  "content": "Konten yang diupdate"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Article updated successfully"
}
```

---

### **5. Delete News**

Hapus artikel dari Manticore.

```http
DELETE /api/news/{news_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Article deleted successfully"
}
```

---

## 📊 Database Schema

### **MySQL Tables**

#### **articles**
```sql
CREATE TABLE articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content TEXT,
    category VARCHAR(100),
    published_at DATETIME
);
```

#### **views**
```sql
CREATE TABLE views (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    article_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Manticore Index**

```sql
CREATE TABLE articles (
    id INTEGER,
    article_id INTEGER,
    embedding_vector FLOAT_VECTOR KNN_TYPE='HNSW' KNN_DIMS=384 HNSW_SIMILARITY='COSINE'
) MODEL_NAME='sentence-transformers/all-MiniLM-L6-v2';
```

**Konfigurasi:**
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensi:** 384
- **KNN Type:** HNSW (Hierarchical Navigable Small World)
- **Similarity:** Cosine similarity

---

## 🔧 Configuration

### **Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `root` |
| `DB_ROOT_PASSWORD` | MySQL password | `password` |
| `DB_NAME` | Database name | `rec` |
| `MANTICORE_HOST` | Manticore host | `localhost` |
| `MANTICORE_PORT` | Manticore HTTP port | `9308` |

---

## 🧪 Testing

### Test Health Check
```bash
curl http://localhost:8000/health
```

### Test Recommendation
```bash
# Pastikan user ID 1 punya reading history
curl http://localhost:8000/api/recommendation/1?limit=10
```

---

## 📁 Project Structure

```
recommendation/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── api/                       # API routes
│   ├── services/                  # Business logic
│   │   └── recommendation_service.py
│   ├── repositories/              # Data access layer
│   │   ├── article_repository.py
│   │   └── manticore_repository.py
│   ├── models/                    # SQLModel models
│   │   └── Article.py
│   └── configs/                   # Configuration
│       ├── db.py
│       └── manticore.py
├── migrations/                    # Database migrations
│   ├── 001_init_mysql.sql
│   └── 002_init_manticore.sql
├── docker-compose.yaml            # Docker services
├── .env                           # Environment variables
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🐛 Troubleshooting

### MySQL Connection Error

**Jika menggunakan Docker:**
```bash
# Check if MySQL is running
docker ps

# Restart MySQL
docker-compose restart mysql

# Check logs
docker logs <mysql-container-id>
```

**Jika instalasi manual:**
```bash
# Check MySQL status
sudo systemctl status mysql  # Linux
brew services info mysql     # macOS

# Restart MySQL
sudo systemctl restart mysql  # Linux
brew services restart mysql   # macOS

# Check logs
sudo tail -f /var/log/mysql/error.log  # Linux
tail -f /opt/homebrew/var/mysql/*.err  # macOS
```

### Manticore Connection Error

**Jika menggunakan Docker:**
```bash
# Check Manticore logs
docker logs <manticore-container-id>

# Restart Manticore
docker-compose restart manticore
```

**Jika instalasi manual:**
```bash
# Check Manticore status
sudo systemctl status manticore  # Linux
brew services info manticoresearch  # macOS

# Restart Manticore
sudo systemctl restart manticore  # Linux
brew services restart manticoresearch  # macOS

# Check logs
sudo tail -f /var/log/manticore/searchd.log  # Linux
tail -f /opt/homebrew/var/log/manticore/searchd.log  # macOS
```

**Test Connection (untuk semua):**
```bash
# Test Manticore HTTP API
curl http://localhost:9308/sql -d "SHOW TABLES"

# Test Manticore SQL port
mysql -h 127.0.0.1 -P 9306 -e "SHOW TABLES"
```

### Empty Recommendations
- Pastikan user memiliki reading history
- Pastikan artikel sudah di-sync ke Manticore
- Check: `SELECT COUNT(*) FROM articles` di Manticore

---

## 📝 License

MIT License

---

## 👥 Contributors

- Muhammad Hakim

---

## 📧 Contact

Untuk pertanyaan atau feedback, silakan buka issue di repository ini.
