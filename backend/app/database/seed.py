"""
Database seed script - migrates data from data_service.py to SQLite database.
Run with: python -m app.database.seed
"""
from sqlalchemy.orm import Session
from .connection import engine, SessionLocal
from ..models.db_models import Base, Profile, SkillCategory, Skill, Project, RoleEmphasis


def get_initial_data():
    """Return the initial data to seed (same structure as data_service.py)."""
    profile_data = {
        "name": "PHAM THE SON",
        "name_kana": "ファム テ ソン",
        "name_vi": "PHẠM THẾ SƠN",
        "gender": "male",
        "date_of_birth": "1997-02-19",
        "school": "ECCコンピュータ専門学校",
        "graduation_year": 2022,
        "field": "WEB開発（フルスタック）、システム開発",
        "work_experience": "4年",
        "japan_residence": "9年",
        "japanese_level": "N2",
        "email": "ptheson1902@gmail.com",
        "phone": "080-1234-5678",
        "address": {
            "ja": "大阪府大阪市",
            "vi": "Thành phố Osaka, Osaka",
            "en": "Osaka City, Osaka"
        },
        "social_links": {
            "facebook": "https://www.facebook.com/ptheson1902",
            "messenger": "https://m.me/ptheson1902",
            "github": "https://github.com/ptheson1902"
        },
        "self_pr": {
            "ja": """【強み】チームリーダー × BrSE × フルスタック × AI開発

■ 経歴
2017年にベトナムから来日。日本語学校（2年）→ ECCコンピュータ専門学校（3年）を経て、日系IT企業で1年間の実務経験を積みました。現在はベトナム系IT企業（3年目）にて、日本向けプロジェクトを担当しています。

■ リーダーシップ経験
直近のAIを活用した自動レジ精算システムでは、5名のチームリーダーとして基本設計から運用保守まで一貫して担当。技術選定、アーキテクチャ設計、コードレビュー、メンバー育成を通じて、プロジェクトを成功に導きました。

■ BrSE（ブリッジSE）経験
日本の顧客とベトナムオフショアチームの橋渡し役として、要件定義から品質管理まで担当。9年間の日本在住経験とN2レベルの日本語力を活かし、日越間のスムーズなコミュニケーションを実現しています。

■ フルスタック開発力
フロントエンド（VueJS, React）からバックエンド（ASP.NET Core, Laravel, Django）、データベース（Oracle, MySQL, SQL Server）まで幅広く対応。高速道路情報管理システムでは、詳細設計から現地試験・運用保守まで全工程を経験しました。

■ AI/ML実践経験
YOLOによるリアルタイム物体検出、Qdrant Vector DBによるベクトル検索、ByteTrackによるオブジェクトトラッキング、WebRTCによるリアルタイム映像配信など、最新のAI技術を実務で活用しています。

■ 目指す姿
技術力とコミュニケーション力を両立し、日本とベトナムの架け橋となりながら、チームとプロダクトの成長に貢献できるエンジニアを目指しています。""",
            "vi": """【Điểm mạnh】Team Leader × BrSE × Fullstack × AI Development

■ Quá trình
Đến Nhật năm 2017. Trường tiếng Nhật (2 năm) → Trường chuyên môn ECC Computer (3 năm) → Công ty IT Nhật Bản (1 năm). Hiện tại đang làm việc tại công ty IT Việt Nam (năm thứ 3), phụ trách các dự án cho khách hàng Nhật Bản.

■ Kinh nghiệm Leadership
Trong dự án Hệ thống thanh toán tự động AI gần đây nhất, với vai trò Team Leader của nhóm 5 người, tôi phụ trách từ thiết kế cơ bản đến vận hành bảo trì. Dẫn dắt dự án thành công thông qua lựa chọn công nghệ, thiết kế kiến trúc, code review và đào tạo thành viên.

■ Kinh nghiệm BrSE (Bridge SE)
Là cầu nối giữa khách hàng Nhật Bản và đội offshore Việt Nam, phụ trách từ định nghĩa yêu cầu đến quản lý chất lượng. Với 9 năm sống tại Nhật và trình độ tiếng Nhật N2, tôi đảm bảo giao tiếp suôn sẻ giữa Nhật-Việt.

■ Năng lực Fullstack
Có khả năng xử lý từ Frontend (VueJS, React) đến Backend (ASP.NET Core, Laravel, Django) và Database (Oracle, MySQL, SQL Server). Trong dự án Hệ thống quản lý thông tin đường cao tốc, tôi đã trải nghiệm toàn bộ quy trình từ thiết kế chi tiết đến thử nghiệm thực tế và vận hành bảo trì.

■ Kinh nghiệm AI/ML thực tế
Ứng dụng các công nghệ AI tiên tiến trong thực tế: phát hiện vật thể real-time bằng YOLO, tìm kiếm vector với Qdrant Vector DB, object tracking với ByteTrack, streaming video real-time với WebRTC.

■ Mục tiêu
Trở thành kỹ sư có thể đóng góp cho sự phát triển của team và sản phẩm, kết hợp năng lực kỹ thuật và khả năng giao tiếp, làm cầu nối giữa Nhật Bản và Việt Nam.""",
            "en": """【Strengths】Team Leader × BrSE × Fullstack × AI Development

■ Career Path
Came to Japan in 2017. Japanese Language School (2 years) → ECC Computer College (3 years) → Japanese IT Company (1 year). Currently working at a Vietnamese IT company (3rd year), handling projects for Japanese clients.

■ Leadership Experience
In the recent AI-powered Automatic Checkout System project, I led a team of 5 as Team Leader, handling everything from basic design to operation & maintenance. Successfully delivered the project through technology selection, architecture design, code review, and team mentoring.

■ BrSE (Bridge SE) Experience
Served as a bridge between Japanese clients and Vietnamese offshore team, responsible for requirements definition to quality management. With 9 years in Japan and N2 Japanese proficiency, I ensure smooth Japan-Vietnam communication.

■ Fullstack Development
Capable of handling Frontend (VueJS, React) to Backend (ASP.NET Core, Laravel, Django) and Database (Oracle, MySQL, SQL Server). In the Highway Information Management System, I experienced the entire process from detailed design to on-site testing and operation maintenance.

■ Practical AI/ML Experience
Applying cutting-edge AI technologies in production: real-time object detection with YOLO, vector search with Qdrant Vector DB, object tracking with ByteTrack, real-time video streaming with WebRTC.

■ Vision
I aim to be an engineer who contributes to team and product growth, combining technical skills with communication abilities, while serving as a bridge between Japan and Vietnam."""
        }
    }

    skills_data = {
        "programming_languages": [
            {"name": "C#", "level": 4, "experience": "2年7ヶ月"},
            {"name": "JavaScript", "level": 4, "experience": "3年5ヶ月"},
            {"name": "PHP", "level": 3, "experience": "9ヶ月"},
            {"name": "Python", "level": 3, "experience": "1年"},
            {"name": "Java", "level": 3, "experience": "8ヶ月"},
            {"name": "VB.NET", "level": 3, "experience": "8ヶ月"},
        ],
        "frameworks": [
            {"name": "ASP.NET Core", "level": 4, "experience": "1年1ヶ月"},
            {"name": "VueJS", "level": 3, "experience": "1年6ヶ月"},
            {"name": "Laravel", "level": 3, "experience": "9ヶ月"},
            {"name": "ASP.NET MVC", "level": 3, "experience": "7ヶ月"},
            {"name": "NodeJS", "level": 2, "experience": "6ヶ月"},
            {"name": "ReactJS", "level": 2, "experience": "6ヶ月"},
            {"name": "Django", "level": 2, "experience": "2ヶ月"},
        ],
        "databases": [
            {"name": "MySQL", "level": 4, "experience": "2年6ヶ月"},
            {"name": "Oracle", "level": 4, "experience": "2年5ヶ月"},
            {"name": "SQL Server", "level": 3, "experience": "10ヶ月"},
            {"name": "PostgreSQL", "level": 3, "experience": "9ヶ月"},
            {"name": "MongoDB", "level": 1, "experience": "6ヶ月"},
        ],
        "cloud": [
            {"name": "Azure", "level": 2, "experience": "9ヶ月"},
        ],
        "ai_ml": [
            {"name": "PyTorch", "level": 3, "experience": "9ヶ月"},
            {"name": "YOLO", "level": 3, "experience": "9ヶ月"},
            {"name": "OpenCV", "level": 3, "experience": "9ヶ月"},
            {"name": "Qdrant", "level": 3, "experience": "9ヶ月"},
            {"name": "ONNX", "level": 2, "experience": "9ヶ月"},
        ]
    }

    projects_data = [
        {
            "id": 1,
            "name": {"ja": "研修", "vi": "Đào tạo", "en": "Training"},
            "role": "Developer",
            "team_size": "1",
            "technologies": ["Java", "HTML5/CSS3", "JavaScript/jQuery"],
            "environment": "Eclipse",
            "phases": ["製造", "単体テスト"],
            "start_date": "2021-06",
            "end_date": "2021-08",
            "duration": "3ヶ月",
            "description": {
                "ja": "【Java】プログラム基礎の理解、課題アプリの作成\n【Oracle】SQLの理解",
                "vi": "【Java】Hiểu cơ bản về lập trình, tạo ứng dụng bài tập\n【Oracle】Hiểu SQL",
                "en": "[Java] Understanding programming basics, creating practice applications\n[Oracle] Understanding SQL"
            },
            "highlights": {
                "ja": ["Javaプログラミングの基礎習得", "SQLの基本操作"],
                "vi": ["Nắm vững cơ bản Java", "Thao tác SQL cơ bản"],
                "en": ["Mastered Java programming basics", "Basic SQL operations"]
            },
            "relevance": {"leader": 1, "brse": 1, "fullstack": 2}
        },
        {
            "id": 2,
            "name": {
                "ja": "営業日報システム開発(WEB)",
                "vi": "Phát triển hệ thống báo cáo kinh doanh hàng ngày (WEB)",
                "en": "Sales Daily Report System Development (WEB)"
            },
            "role": "Developer",
            "team_size": "1",
            "technologies": ["Java", "HTML5/Bootstrap", "JavaScript/jQuery", "Servlet"],
            "environment": "Servlet",
            "phases": ["製造", "単体テスト"],
            "start_date": "2021-09",
            "end_date": "2022-01",
            "duration": "5ヶ月",
            "description": {
                "ja": "入力画面の新規開発を担当しました。新規登録、修正、削除、照会の画面を作成しました。入力に必須なマスタメンテナンス画面についても対応しました。",
                "vi": "Phụ trách phát triển mới màn hình nhập liệu. Đã tạo các màn hình đăng ký mới, sửa đổi, xóa, và tra cứu. Cũng đã xử lý màn hình bảo trì master cần thiết cho việc nhập liệu.",
                "en": "Responsible for new development of input screens. Created screens for new registration, modification, deletion, and inquiry. Also handled master maintenance screens required for input."
            },
            "highlights": {
                "ja": ["CRUD機能の実装", "マスタメンテナンス画面の開発"],
                "vi": ["Triển khai chức năng CRUD", "Phát triển màn hình bảo trì master"],
                "en": ["CRUD functionality implementation", "Master maintenance screen development"]
            },
            "relevance": {"leader": 2, "brse": 2, "fullstack": 4}
        },
        {
            "id": 3,
            "name": {
                "ja": "勤怠（打刻）システム開発(WEB)",
                "vi": "Phát triển hệ thống chấm công (WEB)",
                "en": "Attendance System Development (WEB)"
            },
            "role": "Developer",
            "team_size": "2",
            "technologies": ["C#", "HTML5/Bootstrap", "JavaScript/jQuery", "ASP.NET"],
            "environment": "ASP.NET",
            "phases": ["製造", "単体テスト"],
            "start_date": "2022-01",
            "end_date": "2022-07",
            "duration": "7ヶ月",
            "description": {
                "ja": "画面の新規開発を担当しました。（新規登録、照会の画面の作成）バッチの作成も担当しました。",
                "vi": "Phụ trách phát triển mới màn hình. (Tạo màn hình đăng ký mới, tra cứu) Cũng phụ trách tạo batch.",
                "en": "Responsible for new screen development. (Creating new registration, inquiry screens) Also responsible for batch creation."
            },
            "highlights": {
                "ja": ["新規画面開発", "バッチ処理の実装"],
                "vi": ["Phát triển màn hình mới", "Triển khai xử lý batch"],
                "en": ["New screen development", "Batch processing implementation"]
            },
            "relevance": {"leader": 2, "brse": 2, "fullstack": 4}
        },
        {
            "id": 4,
            "name": {
                "ja": "案件・要員の管理システム(WEB)",
                "vi": "Hệ thống quản lý dự án và nhân sự (WEB)",
                "en": "Project & Resource Management System (WEB)"
            },
            "role": "Developer",
            "team_size": "2",
            "technologies": ["Python", "HTML5/Bootstrap", "JavaScript/jQuery", "ExcelVBA", "Django"],
            "environment": "Django",
            "phases": ["製造", "単体テスト", "詳細設計"],
            "start_date": "2022-06",
            "end_date": "2022-08",
            "duration": "3ヶ月",
            "description": {
                "ja": "ゲスト利用画面の新規開発を担当しました。（新規登録、照会、検索の画面の作成）DB更新、開発環境の作成",
                "vi": "Phụ trách phát triển mới màn hình sử dụng cho khách. (Tạo màn hình đăng ký mới, tra cứu, tìm kiếm) Cập nhật DB, tạo môi trường phát triển",
                "en": "Responsible for new development of guest usage screens. (Creating new registration, inquiry, search screens) DB update, development environment setup"
            },
            "highlights": {
                "ja": ["詳細設計への参加", "開発環境構築"],
                "vi": ["Tham gia thiết kế chi tiết", "Xây dựng môi trường phát triển"],
                "en": ["Participated in detailed design", "Development environment setup"]
            },
            "relevance": {"leader": 3, "brse": 2, "fullstack": 4}
        },
        {
            "id": 5,
            "name": {
                "ja": "賃貸システム開発(Windows)",
                "vi": "Phát triển hệ thống cho thuê (Windows)",
                "en": "Rental System Development (Windows)"
            },
            "role": "Developer",
            "team_size": "10",
            "technologies": ["VB.NET", "List Creator", "INTARFRM"],
            "environment": "Windows (Fujitsu)",
            "phases": ["製造", "単体テスト", "詳細設計"],
            "start_date": "2022-08",
            "end_date": "2023-03",
            "duration": "8ヶ月",
            "description": {
                "ja": "不動産のシステム開発、案件対応",
                "vi": "Phát triển hệ thống bất động sản, xử lý các yêu cầu dự án",
                "en": "Real estate system development, handling project requirements"
            },
            "highlights": {
                "ja": ["大規模チームでの開発経験", "不動産ドメイン知識の習得"],
                "vi": ["Kinh nghiệm phát triển trong nhóm lớn", "Học hỏi kiến thức lĩnh vực bất động sản"],
                "en": ["Development experience in large team", "Acquired real estate domain knowledge"]
            },
            "relevance": {"leader": 3, "brse": 3, "fullstack": 3}
        },
        {
            "id": 6,
            "name": {
                "ja": "住宅管理システムのリプレース",
                "vi": "Thay thế hệ thống quản lý nhà ở",
                "en": "Housing Management System Replacement"
            },
            "role": "Developer",
            "team_size": "5",
            "technologies": ["VueJS"],
            "environment": "Visual Studio Code",
            "phases": ["デザイン", "製造"],
            "start_date": "2023-04",
            "end_date": "2023-05",
            "duration": "2ヶ月",
            "description": {
                "ja": "モックアップ作成を担当しました。",
                "vi": "Phụ trách tạo mockup.",
                "en": "Responsible for creating mockups."
            },
            "highlights": {
                "ja": ["UI/UXデザイン", "フロントエンド設計"],
                "vi": ["Thiết kế UI/UX", "Thiết kế frontend"],
                "en": ["UI/UX design", "Frontend design"]
            },
            "relevance": {"leader": 2, "brse": 2, "fullstack": 4}
        },
        {
            "id": 7,
            "name": {
                "ja": "実習生＆特定技能管理システム",
                "vi": "Hệ thống quản lý thực tập sinh và kỹ năng đặc định",
                "en": "Trainee & Specified Skilled Worker Management System"
            },
            "role": "Sub-BrSE",
            "team_size": "7",
            "technologies": ["C#", "JavaScript", "ASP.NET MVC", "VueJS"],
            "environment": "ASP.NET MVC, VueJS",
            "phases": ["結合テスト", "Q&A対応", "詳細設計"],
            "start_date": "2023-06",
            "end_date": "2023-11",
            "duration": "6ヶ月",
            "description": {
                "ja": "帳票作成、更新、出力（Excel, PDF）。データ登録：CSVインポート、マスター登録、一括登録、複製登録、母国語対応",
                "vi": "Tạo, cập nhật, xuất báo cáo (Excel, PDF). Đăng ký dữ liệu: Import CSV, đăng ký master, đăng ký hàng loạt, đăng ký sao chép, hỗ trợ ngôn ngữ mẹ đẻ",
                "en": "Report creation, update, output (Excel, PDF). Data registration: CSV import, master registration, bulk registration, copy registration, native language support"
            },
            "highlights": {
                "ja": ["Sub-BrSEとしての初めての経験", "帳票機能の実装", "多言語対応"],
                "vi": ["Kinh nghiệm đầu tiên với vai trò Sub-BrSE", "Triển khai chức năng báo cáo", "Hỗ trợ đa ngôn ngữ"],
                "en": ["First experience as Sub-BrSE", "Report functionality implementation", "Multi-language support"]
            },
            "relevance": {"leader": 3, "brse": 5, "fullstack": 4}
        },
        {
            "id": 8,
            "name": {
                "ja": "高速道路情報管理システム",
                "vi": "Hệ thống quản lý thông tin đường cao tốc",
                "en": "Highway Information Management System"
            },
            "role": "Developer",
            "team_size": "6",
            "technologies": ["C#", "JavaScript", "ASP.NET Core", "Oracle", "SQL Server"],
            "environment": "ASP.NET Core, Oracle, SQL Server",
            "phases": ["詳細設計", "コーディング", "製造", "単体テスト", "結合テスト", "総合試験", "現地試験", "運用・保守"],
            "start_date": "2023-12",
            "end_date": "2024-12",
            "duration": "1年1ヶ月",
            "description": {
                "ja": "交通管制データの連携及び活用：データ管理、帳票やCSVやPDFなど出力。データ統計：データ管理、帳票やCSVやPDFなど出力。道路状況：地図上のストリームカメラの管理。無線局管理：XMLファイル作成、申請履歴の管理、納付情報の管理、ユーザ情報の管理。バッチ改善を担当しました。",
                "vi": "Liên kết và sử dụng dữ liệu điều khiển giao thông: Quản lý dữ liệu, xuất báo cáo/CSV/PDF. Thống kê dữ liệu. Tình trạng đường: Quản lý camera stream trên bản đồ. Quản lý trạm vô tuyến: Tạo file XML, quản lý lịch sử đăng ký, quản lý thông tin thanh toán, quản lý thông tin người dùng. Cải thiện batch.",
                "en": "Traffic control data integration and utilization: Data management, report/CSV/PDF output. Data statistics. Road conditions: Stream camera management on maps. Radio station management: XML file creation, application history management, payment info management, user info management. Batch improvement."
            },
            "highlights": {
                "ja": ["フルスタック開発", "現地試験対応", "運用保守経験", "大規模システム"],
                "vi": ["Phát triển fullstack", "Đối ứng thử nghiệm tại chỗ", "Kinh nghiệm vận hành bảo trì", "Hệ thống quy mô lớn"],
                "en": ["Fullstack development", "On-site testing", "Operation & maintenance experience", "Large-scale system"]
            },
            "relevance": {"leader": 4, "brse": 3, "fullstack": 5}
        },
        {
            "id": 9,
            "name": {
                "ja": "人物・人事管理システム",
                "vi": "Hệ thống quản lý nhân sự",
                "en": "Personnel & HR Management System"
            },
            "role": "BrSE",
            "team_size": "6",
            "technologies": ["C#", "JavaScript", ".NET MVC", "Oracle"],
            "environment": ".NET MVC, Oracle",
            "phases": ["コーディング", "単体テスト", "製造", "Q&A対応"],
            "start_date": "2025-01",
            "end_date": "2025-06",
            "duration": "6ヶ月",
            "description": {
                "ja": "日本の顧客とオフショア開発チームのブリッジとして、要件定義、技術的な伝達、品質管理、日越間のコミュニケーションを担当。人物調査管理画面を担当。人事評価管理画面を担当。調査評価基準設定管理を担当。",
                "vi": "Là cầu nối giữa khách hàng Nhật Bản và đội phát triển offshore, phụ trách định nghĩa yêu cầu, truyền đạt kỹ thuật, quản lý chất lượng, giao tiếp Nhật-Việt. Phụ trách màn hình quản lý điều tra nhân vật. Phụ trách màn hình quản lý đánh giá nhân sự. Phụ trách quản lý cài đặt tiêu chí đánh giá điều tra.",
                "en": "As a bridge between Japanese clients and offshore development team, responsible for requirements definition, technical communication, quality management, Japan-Vietnam communication. Responsible for personnel investigation management screen. HR evaluation management screen. Investigation evaluation criteria setting management."
            },
            "highlights": {
                "ja": ["BrSEとしての本格的な経験", "要件定義", "日越間コミュニケーション", "品質管理"],
                "vi": ["Kinh nghiệm chính thức với vai trò BrSE", "Định nghĩa yêu cầu", "Giao tiếp Nhật-Việt", "Quản lý chất lượng"],
                "en": ["Full BrSE experience", "Requirements definition", "Japan-Vietnam communication", "Quality management"]
            },
            "relevance": {"leader": 4, "brse": 5, "fullstack": 3}
        },
        {
            "id": 10,
            "name": {
                "ja": "AIを活用した自動レジ精算システム",
                "vi": "Hệ thống thanh toán tự động sử dụng AI",
                "en": "AI-Powered Automatic Checkout System"
            },
            "role": "Team Leader",
            "team_size": "5",
            "technologies": ["PHP", "VueJS", "Python", "Laravel", "PyTorch", "ONNX", "YOLO", "Qdrant", "OpenCV", "WebSockets", "MySQL"],
            "environment": "Laravel, PyTorch, ONNX, YOLO, Qdrant, OpenCV, WebSockets, MySQL",
            "phases": ["基本設計", "詳細設計", "コーディング", "単体テスト", "結合テスト", "運用・保守"],
            "start_date": "2025-06",
            "end_date": "2026-02",
            "duration": "9ヶ月",
            "description": {
                "ja": "USBカメラで撮影した商品画像をリアルタイムで認識・分類し、レジ精算を自動化するエッジAIシステム。主な機能：YOLOベースのリアルタイム商品検出、ベクトル埋め込みによる商品分類（Qdrant Vector DB）、ByteTrackによるマルチオブジェクトトラッキング、WebRTCによるリアルタイム映像配信、クラウド同期機能（商品データベース同期）、商品登録機能（新商品の画像登録・学習）",
                "vi": "Hệ thống Edge AI nhận dạng và phân loại hình ảnh sản phẩm quay bằng camera USB theo thời gian thực, tự động hóa thanh toán. Chức năng chính: Phát hiện sản phẩm thời gian thực dựa trên YOLO, Phân loại sản phẩm bằng vector embedding (Qdrant Vector DB), Theo dõi đa đối tượng bằng ByteTrack, Phát video thời gian thực bằng WebRTC, Đồng bộ cloud, Đăng ký sản phẩm mới",
                "en": "Edge AI system that recognizes and classifies product images captured by USB camera in real-time, automating checkout. Main features: YOLO-based real-time product detection, Product classification by vector embedding (Qdrant Vector DB), Multi-object tracking with ByteTrack, Real-time video streaming via WebRTC, Cloud sync functionality, New product registration and training"
            },
            "highlights": {
                "ja": ["チームリーダーとしての経験", "AI/ML技術の実践", "システム設計", "フルスタック開発"],
                "vi": ["Kinh nghiệm làm Team Leader", "Thực hành công nghệ AI/ML", "Thiết kế hệ thống", "Phát triển fullstack"],
                "en": ["Team Leader experience", "AI/ML technology practice", "System design", "Fullstack development"]
            },
            "relevance": {"leader": 5, "brse": 3, "fullstack": 5}
        }
    ]

    role_emphasis = {
        "leader": {
            "ja": ["システム設計・アーキテクチャ", "チームマネジメント", "技術的意思決定", "コードレビュー・メンタリング", "品質・納期管理"],
            "vi": ["Thiết kế hệ thống & kiến trúc", "Quản lý nhóm", "Ra quyết định kỹ thuật", "Code review & hướng dẫn", "Quản lý chất lượng & tiến độ"],
            "en": ["System design & architecture", "Team management", "Technical decision making", "Code review & mentoring", "Quality & delivery management"]
        },
        "brse": {
            "ja": ["日本語コミュニケーション", "要件定義・仕様策定", "顧客対応", "ドキュメント作成", "日越間の調整"],
            "vi": ["Giao tiếp tiếng Nhật", "Định nghĩa yêu cầu & đặc tả", "Đối ứng khách hàng", "Tạo tài liệu", "Điều phối Nhật-Việt"],
            "en": ["Japanese communication", "Requirements definition", "Customer interaction", "Documentation", "Japan-Vietnam coordination"]
        },
        "fullstack": {
            "ja": ["フロントエンド開発", "バックエンド開発", "API設計", "データベース設計", "クラウド・DevOps"],
            "vi": ["Phát triển Frontend", "Phát triển Backend", "Thiết kế API", "Thiết kế Database", "Cloud & DevOps"],
            "en": ["Frontend development", "Backend development", "API design", "Database design", "Cloud & DevOps"]
        }
    }

    return profile_data, skills_data, projects_data, role_emphasis


def seed_database():
    """Seed the database with initial data."""
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    profile_data, skills_data, projects_data, role_emphasis_data = get_initial_data()

    try:
        # 1. Seed Profile (only if not exists)
        if not db.query(Profile).first():
            profile = Profile(
                id=1,
                name=profile_data["name"],
                name_kana=profile_data["name_kana"],
                name_vi=profile_data["name_vi"],
                gender=profile_data["gender"],
                date_of_birth=profile_data["date_of_birth"],
                school=profile_data["school"],
                graduation_year=profile_data["graduation_year"],
                field=profile_data["field"],
                work_experience=profile_data["work_experience"],
                japan_residence=profile_data["japan_residence"],
                japanese_level=profile_data["japanese_level"],
                email=profile_data["email"],
                phone=profile_data["phone"],
                address=profile_data["address"],
                social_links=profile_data["social_links"],
                self_pr=profile_data["self_pr"]
            )
            db.add(profile)
            print("✓ Profile seeded")

        # 2. Seed Skill Categories and Skills
        category_order = {
            "programming_languages": 1,
            "frameworks": 2,
            "databases": 3,
            "cloud": 4,
            "ai_ml": 5
        }

        for cat_key, order in category_order.items():
            existing_cat = db.query(SkillCategory).filter(SkillCategory.key == cat_key).first()
            if not existing_cat:
                category = SkillCategory(key=cat_key, display_order=order)
                db.add(category)
                db.flush()  # Get the category ID

                for i, skill_data in enumerate(skills_data.get(cat_key, [])):
                    skill = Skill(
                        name=skill_data["name"],
                        level=skill_data["level"],
                        experience=skill_data["experience"],
                        category_id=category.id,
                        category_key=cat_key,
                        display_order=i
                    )
                    db.add(skill)
                print(f"✓ {cat_key} skills seeded")

        # 3. Seed Projects
        for proj_data in projects_data:
            existing_proj = db.query(Project).filter(Project.id == proj_data["id"]).first()
            if not existing_proj:
                project = Project(
                    id=proj_data["id"],
                    name=proj_data["name"],
                    description=proj_data["description"],
                    highlights=proj_data["highlights"],
                    role=proj_data["role"],
                    team_size=proj_data["team_size"],
                    technologies=proj_data["technologies"],
                    environment=proj_data["environment"],
                    phases=proj_data["phases"],
                    start_date=proj_data["start_date"],
                    end_date=proj_data.get("end_date"),
                    duration=proj_data["duration"],
                    relevance_leader=proj_data["relevance"]["leader"],
                    relevance_brse=proj_data["relevance"]["brse"],
                    relevance_fullstack=proj_data["relevance"]["fullstack"],
                    display_order=proj_data["id"]
                )
                db.add(project)
        print("✓ Projects seeded")

        # 4. Seed Role Emphasis
        for role_key, keywords in role_emphasis_data.items():
            existing_emphasis = db.query(RoleEmphasis).filter(RoleEmphasis.role == role_key).first()
            if not existing_emphasis:
                emphasis = RoleEmphasis(role=role_key, keywords=keywords)
                db.add(emphasis)
        print("✓ Role emphasis seeded")

        db.commit()
        print("\n✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


def reset_database():
    """Drop all tables and recreate them."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset complete")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
        seed_database()
    else:
        seed_database()
