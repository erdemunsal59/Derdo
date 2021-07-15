	Etiket-Aracı

Python Tkinter ile uygulanan, görüntülerdeki nesne sınırlayıcı kutuları etiketlemek için kullanılan bir araç.
Aracı çalıştırmak için Terminale "python main.py" yazıp enter tuşuna basmanız yeterlidir.

Etiket Aracı

-main.py # Araç için kaynak kod

-etiket.txt # Etiketler için sınıflar

-Images/ # Etiketlenecek görüntüleri içeren dizin

-Labels/ # Etiketleme sonuçları için dizin

-Examples/ # Örnek için dizin

Bu program şunları içeriyor:

-Giriş görüntüleri.
-Çıkış etiketleri.
-Bu dizinleri Görüntü giriş klasörü ve Etiket çıktı klasörü olarak seçebilir veya girişte dizin adını girebilirsiniz.

1. Görüntü yükle'ye tıklayın. Etiketlenecek resimlerin bulunduğu klasörü seçin. Klasörde etiketlenecek resimler, örnek sonuçla birlikte yüklenecektir. 
Etiketli dosya dizini, mevcut değilse otomatik olarak oluşturulur.
2. Yeni bir sınırlayıcı kutu oluşturmak için, ilk noktayı seçmek için sol tıklayın. 
Bir dikdörtgen çizmek için fareyi hareket ettirin ve ikinci noktayı seçmek için tekrar sol tıklayın.
Çizim sırasında sınırlayıcı kutuyu iptal etmek için <Esc> tuşuna basmanız yeterlidir.
Mevcut bir sınırlayıcı kutuyu silmek için liste kutusundan seçin ve Sil'e tıklayın.
Görüntüdeki mevcut tüm sınırlayıcı kutuları silmek için Tümünü Sil'e tıklamanız yeterlidir.
3. Bir görüntüyü bitirdikten sonra, ilerlemek için Sonraki Resim'e tıklayın. Aynı şekilde bir önceki görüntüye gitmek için Önceki Resim öğesine tıklayın veya 
bir resim numarası girin ve belirtilen resme gitmek için Git'e tıklayın. Bir görüntüyü bitirdikten sonra Sonraki Resim'e veya Önceki Resim'e tıkladığınızdan emin olun, 
aksi takdirde sonuç kaydedilmez. Önceki resme gitmek için 'p' tuşuna basın, Sonraki resme gitmek için 'n' düğmesine basın.
4. Görüntü ekrana sığmazsa, program hem sınırlayıcı kutuyu, hem de yükleme sırasında görüntüyü yeniden boyutlandırır.
5. Farklı görüntüler etiketlemek için, 'etiket.txt' dosyasını kendi etiket adaylarınızla değiştirin ve görüntüyü etiketlemeden önce 
Etiket Aracı'nda 'Etiketi Belirle'yi seçin ve düğmesini tıkladığınızdan emin olun.
6. Görüntü dosya adı yolda.giden.araba.jpg formatında ise, etiketli dosya adı yolda.giden.araba.txt olur, yolda.txt değil.
7. Birden fazla görüntü biçimini destekler bunlar: "*.JPEG", "*.jpeg", "*JPG", "*.jpg", "*.PNG", "*.png", "*.BMP", "*.bmp ".
