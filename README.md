# Απλό Blog με Flask + SQLite

## Περιγραφή
Ένα απλό blog application με Flask και SQLite database. Αυτή είναι η **βασική έκδοση χωρίς security features**.

## Λειτουργίες
- ✅ Προβολή όλων των posts (αρχική σελίδα)
- ✅ Δημιουργία νέου post
- ✅ Προβολή πλήρους post
- ✅ Διαγραφή post
- ✅ SQLite database

## Δομή Project

```
blog/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── blog.db                 # SQLite database (δημιουργείται αυτόματα)
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Homepage με λίστα posts
    ├── new_post.html      # Φόρμα νέου post
    └── post.html          # Προβολή πλήρους post
```

## Εγκατάσταση

1. Εγκατάσταση dependencies:
```bash
pip install -r requirements.txt
```

2. Εκτέλεση εφαρμογής:
```bash
python app.py
```

3. Άνοιξε το browser στο: `http://localhost:5000`

## Database Schema

**Table: posts**
- id (INTEGER PRIMARY KEY)
- title (TEXT)
- content (TEXT)
- author (TEXT)
- created_at (TIMESTAMP)

## Επόμενα Βήματα (Security Features)

Αυτή η έκδοση είναι η **βασική χωρίς security**. Θα προσθέσουμε στη συνέχεια:

1. ✋ Μελέτη ασφάλειας (Risk Analysis + Security Policy)
2. 🔒 SSL/HTTPS με πιστοποιητικό
3. 🔑 Authentication & Authorization
4. 🛡️ Input validation & filtering (SQL injection, XSS protection)
5. 🔍 Vulnerability scanning (ZAP/OpenVAS)
6. 📋 Τελική μελέτη ασφάλειας

## Σημειώσεις

⚠️ **ΠΡΟΣΟΧΗ**: Αυτή η έκδοση δεν είναι ασφαλής και χρησιμοποιείται μόνο ως αρχική βάση.

- Δεν υπάρχει authentication (οποιοσδήποτε μπορεί να δημιουργήσει/διαγράψει posts)
- Δεν υπάρχει input validation (ευάλωτο σε SQL injection, XSS)
- Τρέχει σε HTTP χωρίς encryption
- Debug mode enabled

Όλα αυτά θα διορθωθούν στα επόμενα βήματα!
