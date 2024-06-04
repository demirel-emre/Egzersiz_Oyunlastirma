Egzersiz Oyunlaştırma Uygulaması | Emre DEMİREL

Bu uygulama, fitness egzersizlerini gerçek zamanlı olarak tanıyan ve kullanıcılara geribildirim olarak doğruluk oranı ve skor sağlayan bir sistemdir.
Bu README dosyası, projenin nasıl kullanılacağına ve yapılandırılacağına dair detaylı bilgiler içerir.


Dosyalar ve Klasörler:
- frameayirma.py: Egzersiz videolarından kareler çıkartarak eğitim için veri setini hazırlayan Python betiği.
- fitnessmodel.py: Eğitim için hazırlanan veri seti üzerinde bir CNN modeli eğiten ve fitness egzersizlerini tanıyan bir model oluşturan Python betiği.
- finalmodelcamerarevize2.py: Bu Python betiği, eğitilen modeli gerçek zamanlı olarak kullanıcıların egzersizlerini tanıyan ve geribildirim sağlayan bir kullanıcı arayüzü oluşturur.

Bu arayüz, kullanıcıya iki seçenek sunar: "Yapılan Hareketi Tahmin Et" ve "Hareketler Arasından Seçim Yap".

Yapılan Hareketi Tahmin Et Seçimi:
- Bu seçenek, kullanıcının video seçme veya kamera akışını kullanarak egzersiz yaparken gerçek zamanlı olarak egzersiz türünü tahmin etmesini sağlar.
- Kullanıcı, video dosyasını seçerek veya kamera akışını kullanarak egzersizlerini izleyebilir.
- Kullanıcı, seçilen video dosyası veya kamera akışı, eğitilen model tarafından analiz edilir ve her bir karedeki egzersiz türü tahmin edilir.
- Eğitilen model, egzersiz türünü belirler ve kullanıcıya doğru veya yanlış yapıldığına dair geribildirim sağlar.

Hareketler Arasından Seçim Yap Seçimi:
- Bu seçenek, kullanıcının belirli bir egzersiz türünü seçerek gerçek zamanlı olarak o egzersizi yapmasını sağlar.
- Kullanıcı, bir egzersiz türünü seçer ve ardından “hareket seç” butonu ile hareketi onayladıktan sonra; video seçme veya kamera akışını kullanarak egzersiz yapabilir.
- Seçilen egzersiz türüne göre, eğitilen model egzersiz performansını analiz eder ve kullanıcıya geribildirim sağlar.
- Kullanıcı, egzersiz performansını izleyebilir ve seçilen egzersiz türüne göre gerçek zamanlı doğru veya yanlış yapıldığına dair geribildirim alabilir.
- Kullanıcının kamera açısı ve duruş pozisyonu doğruluk için çok önemlidir.
- Egzersiz performansı, kullanıcının seçtiği egzersiz türüne göre değerlendirilir ve geribildirim sağlanır.

- dataset/: Kendimizin oluşturduğu egzersiz videolarının ve bu videolardan çıkartılan karelerin bulunduğu veri seti.
- fitness_model.h5: Eğitilmiş modelin kaydedildiği model dosyası.

Kullanım:
1. frameayirma.py: Bu betiği kullanarak, egzersiz videolarından kareler çıkartılmalıdır. Çıkartılan kareler eğitim için kullanılacak veri setini oluşturur.
2. fitnessmodel.py: Eğitim için hazırlanan veri seti üzerinde bir CNN modeli eğitiliyor. Eğitilen model, verisetinde bulunan fitness egzersizlerini tanıyan bir model oluşturur. Ve bu model kaydedilir.
3. finalmodelcamerarevize2.py: Eğitilen model, gerçek zamanlı olarak kullanıcıların egzersizlerini tanır ve geribildirim sağlar.
Kullanıcıya "Yapılan Hareketi Tahmin Et" ve "Hareketler Arasından Seçim Yap" olarak iki seçenek sonrası; video seçme veya kamera akışını kullanma seçenekleri sunar.

Gereksinimler:
- Python 3
- OpenCV
- TensorFlow
- Keras
- Mediapipe
- Tkinter
