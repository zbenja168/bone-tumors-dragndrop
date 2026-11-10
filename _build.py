"""Build index.html for the Bone Tumors drag-and-drop (from the student's bone tumor table).
Run: py _build.py   (injects the Active Transport badge from ../msk-labeler/_badge.html)."""
import html, io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
COLS = [
    ("vignette", "Case vignette"), ("bm", "Benign or malignant?"), ("rad", "Radiography"),
    ("histo", "Histomorphology"), ("gen", "Genetics / pathophysiology"), ("tx", "Treatment"),
]
NA = None  # "Not in source" in the table: no card, the slot is shown as a dash
ROWS = [
    {"t": "Metastatic bone cancer",
     "vignette": "A 50- to 58-year-old male with a history of prostate cancer presents with back pain, numbness in the extremities, and pathologic fracture",
     "bm": "Malignant", "rad": "Osteoblastic bone lesion (lesion with increased bony matrix formation)",
     "histo": "Tumor cells arranged into glands (adenocarcinoma)",
     "gen": "Cancer cells releasing growth factors to activate osteoblasts",
     "tx": "Surgical excision; chemotherapy/radiation for metastatic lesions"},
    {"t": "Osteochondroma",
     "vignette": "A 16-year-old male presents with a slow-growing, painless mass around his knee",
     "bm": "Benign", "rad": "Bony exostosis with cartilaginous cap", "histo": "Normal endochondral ossification",
     "gen": "Associated with germline mutations in EXT1 or EXT2",
     "tx": "Observation for small lesions; symptomatic lesions treated with curettage and bone grafting"},
    {"t": "Osteoid osteoma",
     "vignette": "A 15-year-old male presents with dull, aching leg pain that is worse at night and dramatically relieved by NSAIDs",
     "bm": "Benign", "rad": "<1 cm well-circumscribed lytic lesion/tumor with radiolucent osteoid core in the diaphysis of the femur",
     "histo": "Core of osteoid and bone alongside fibrous connective tissue", "gen": NA,
     "tx": "Close monitoring, surgical removal for enlargement, painful lesions"},
    {"t": "Osteoblastoma",
     "vignette": "A 12- to 18-year-old male presents with a 6-month history of progressively worsening upper back pain. The pain is persistent, does not improve significantly with NSAIDs/ibuprofen, and has caused him to develop mild scoliosis",
     "bm": "Benign", "rad": ">2–3 cm well-circumscribed lytic lesion/tumor with osteoid core in vertebrae",
     "histo": "Core of osteoid and bone alongside fibrous connective tissue", "gen": NA,
     "tx": "Surgical removal for severe pain, nerve impingement; radiofrequency ablation"},
    {"t": "Enchondroma",
     "vignette": "A 24-year-old female presents with pain and swelling in her right index finger",
     "bm": "Benign", "rad": "Well-circumscribed radiolucent lesion in medullary cavity of hands/feet",
     "histo": "Composed of hyaline cartilage with benign chondrocytes",
     "gen": "Heterozygous mutations in IDH1 and IDH2 genes. Somatic/multiple mutations can lead to Ollier disease and Maffucci syndrome",
     "tx": "Curettage or en-bloc excision"},
    {"t": "Giant cell tumor of bone",
     "vignette": "A 28-year-old woman presents with a 2- to 4-month history of progressively worsening pain and swelling around her right knee",
     "bm": "Benign", "rad": "Eccentric, lytic, expansile lesion in the distal femur with cortical destruction (“soap bubble” appearance)",
     "histo": "Oval mononuclear tumor cells, osteoclast-like giant cells",
     "gen": "Neoplastic cells overexpress RANKL, leading to recruitment of osteoclast-like giant cells and bone destruction",
     "tx": "Curettage; possible use of RANKL inhibitor denosumab as alternative or adjuvant therapy"},
    {"t": "Chondroblastoma",
     "vignette": "A 14-year-old male presents with a 3-month history of progressive right shoulder pain and decreased range of motion",
     "bm": "Benign", "rad": "Well-circumscribed lytic lesion with a thin sclerotic margin in epiphysis of proximal humerus",
     "histo": "Oval to polygonal chondroblasts with associated purple, “chicken wire” calcification", "gen": NA,
     "tx": "Curettage and bone grafting"},
    {"t": "Osteosarcoma",
     "vignette": "A 15- to 16-year-old boy presents with a 2-month history of worsening pain and swelling in his right knee. The pain has become persistent/constant and progressively/occasionally wakes him at night",
     "bm": "Malignant", "rad": "Mixed lytic and sclerotic lesion in the metaphysis of the distal femur with elevation of the periosteum (Codman’s triangle) and extension into surrounding soft tissue",
     "histo": "Anaplastic tumor cells with production of malignant osteoid",
     "gen": "Risk increased by a history of Paget disease of bone, prior radiation exposure, and inherited cancer syndromes such as RB1/RB gene (familial retinoblastoma) or TP53/p53 (Li-Fraumeni syndrome) mutations",
     "tx": "Neoadjuvant chemotherapy, surgical excision, and postoperative adjuvant chemotherapy; typical MAP (methotrexate, doxorubicin, cisplatin) regimen"},
    {"t": "Chondrosarcoma",
     "vignette": "A 58-year-old male presents with a 6-month history of progressively worsening pain in his left hip",
     "bm": "Malignant", "rad": "Expansile metaphyseal pelvic lesion with cortical destruction and punctate calcifications",
     "histo": "Malignant chondrocytes producing cartilaginous matrix",
     "gen": "15% are secondary and arise from pre-existing enchondromas or osteochondromas",
     "tx": "Surgical excision. Neoadjuvant chemotherapy/radiation is typically ineffective; reserved with or without radiation for dedifferentiated type (typical VDC/IE regimen: vincristine, doxorubicin, cyclophosphamide, ifosfamide, and etoposide)"},
    {"t": "Ewing sarcoma",
     "vignette": "A 12-year-old boy presents with a 5-week history of progressive pain and swelling in his left/high thigh",
     "bm": "Malignant", "rad": "Destructive diaphyseal lesion with characteristic multilayered onion-skin periosteal reaction",
     "histo": "Sheets of round blue cells", "gen": "t(11;22) (EWSR1::FLI1 / EWSR1-FLI1)", "tx": "Chemotherapy/radiation"},
    {"t": "Langerhans cell histiocytosis (LCH)",
     "vignette": "A 5-year-old boy presents with persistent pain and swelling over his scalp. His parents also report a history of a chronic, crusted rash involving the scalp and behind the ears",
     "bm": "Clonal neoplastic disease", "rad": "Lytic lesions in the skull",
     "histo": "Cells with grooved, reniform nuclei admixed with numerous eosinophils; Birbeck granules (tennis racket-like granules on electron microscopy); tumor cells positive for S100 and CD1a",
     "gen": "Associated with BRAF V600E mutations",
     "tx": "Localized disease treated with curettage or topical/intralesional steroid therapy; multiple bone involvement or multisystem/systemic disease requires systemic treatment"},
]

badge = io.open(os.path.join(HERE, "..", "msk-labeler", "_badge.html"), encoding="utf-8").read()
page = io.open(os.path.join(HERE, "_template.html"), encoding="utf-8").read()
page = page.replace("/*DATA*/", "const COLS = " + json.dumps(COLS) + ";\nconst ROWS = " + json.dumps(ROWS, ensure_ascii=False) + ";")
page = page.replace("<!--BADGE-->", badge)
io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print("built index.html:", len(ROWS), "tumors,", sum(1 for r in ROWS for k, _ in COLS if r[k]), "cards")
