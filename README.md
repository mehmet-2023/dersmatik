# Dersmatik
Dersmatik ile tanışın! ortaokul seviyesindeki öğrenciler için hazırlanmış bir ders ajandası sistemi. Ana merkezden yöneten admin bir sınıf açar ve öğrenciler sınıf kodlarıyla sınıflara katılabilir. Öğrenci isterse tek başına kullanabilir.
## Ders Ajandaları
Öğrencinin bir deftere kayıt girerek (veya yayınevlerinden hazırlanmış ajandalar alarak) günlük sorularını yazdığı ve bu soruları analiz ettiği bir kayıt aracıdır. Öğrenciler bir süre sonra "Ne işime yarayacak ki?" diye düşünüp kayıt işlemini bırakabilmektedir. Bu program sadece öğrencinin daha pratik kayıt etmesini sağlamıyor,  öğretmenlerin sınıf içi öğrenci
analizlerine katkıda bulunuyor.
## Kullanım
Uygulamayı iki şekilde kullanabilirsiniz: Firebase anahtarsız veya firebase anahtarlı. Ayrıca pydroid uygulaması ile uygulamayı telefonlarda kullanabilirsiniz.
**Firebase Anahtarı Alma**
Üç program dosyasında da firebase anahtarı istenir. 

 1. Firebase anahtarınızı almanız önce yeni bir [Firebase Projesi](https://console.firebase.google.com/u/0/) oluşturmalısınız.
 2. Proje oluşturulduktan sonra uygulama ekleme kısmına girin ve web seçeneğini seçin. Açılan pencerede istediğiniz adı girin.  Firebase SDK'sını ekle seçeneğini görmezden gelin ve konsola gidin. 
 3.  Sol bölümdeki **Product categories**'deki build kısmını açın ve **Realtime Database**'i seçin veri tabanını olduğu gibi kurun.
 4. Açılan veri tabanınızda yukarıdaki **Rules** seçeneğine gidin. Kuralları şu şekilde düzenleyin:

>     {
>     "rules": {
>     ".read": true,
>     ".write": true,
>     }
>     }

 6. kuralları düzenledikten sonra project overview kısmının yanındaki ayarlar butonuna tıklayın. Ve **Project Settings**'e gidin.
 7. Service accounts bölümüne geçin.
 8. **Generate New Private Key** butonuna tıklayın.
 9. Json dosyasının içeriğini "veri buraya" yazan yere yapıştırın.(üç dosyada da)
 10. **Realtime Database** kısmına geri dönün ve veri tabanı urlsini kopyalayın. Bu urlyi üç dosyada da < url buraya > yazan kısımların yerine yazın. (sadece < url buraya > yazan yeri silin.)
 11. Programı kaydedin ve öğrencilerin kullanımına sunun.

 **Örnek veri tabanlı dosya için bana ulaşmanız yeterlidir.**
 
 # Mobil Kullanım
 Öncelikle telefonunuzun indirilenler klasörüne **Dersmatik** adında bir klasör açın.
 Kaynak kodlarını bu klasöre kopyalayın.
 Pydroid3 uygulamasını kurun.
 Uygulamada terminal sayfasına geçin.
 terminale **pip install tk, firebase_admin, matplotlib, requests, subprocess, json** kodunu yazın. Eğer isterseniz uygulamanın pip kısmından gereksinimleri teker teker yükleyebilirsiniz.
 Üç dosyada da **conn = sqlite3.connect("databases.db")** yazan satırı bulun ve kodu şu şekilde düzeltin:
  >conn = sqlite3.connect("/storage/emulated/0/Download/Dersmatik/databases.db")

*Klasör açmak için ZArchiver kullanabilirsiniz.*
# Bilgisayarda Kullanım
Python 3.11(Opsiyonel) sürümünü kurun ve kurarken **customize installation** 'ı seçerek **Add Python to envoriment varibles** kutucuğunu işaretleyin ve ilerleyerek kurulumu tamamlayın.
Cmd'yi açın - (windows + R) -----> cmd kısayolunu deneyebilirsiniz- ve komut satırına şu kodu girin: **pip install tk, firebase_admin, matplotlib, requests, subprocess, json** .
Programı şimdi kullanabileceksiniz.
### Kurulum işlemini yaparken okulunuzun bilişim bölümünden destek almanızı öneririz.
# Uygulama İşlevi
Uygulama üç ana programdan oluşur: İşlemleri yapabileceğiniz dersmatik.py dosyası, yöneticinin kullanacağı admin.py dosyası ve sınıflara katılabileceğiniz online.py dosyası.  
Sınıf sistemi ile sınıfın ilerlemesini görebilir veya öğrenci sorgulaması yapabilirsiniz.

![Sinif](https://i.ibb.co/nncDmsv/resim-2024-03-02-210433626.png)

Ana program analizler yapmanızı sağlar ve hakkınızda yapılan değerlendirmeleri görebilirsiniz. Haftayı gönder ile verilerinizin admine ulaşmasını sağlarsınız.

![Main](https://i.ibb.co/N9fjPj7/resim-2024-03-02-210711881.png)

Admin programı ile haftalarını gönderen öğrenciler için değerlendirme yazabilirsiniz.
# Lisans
Program MIT Lisansı altındadır. Programı kurumsal olarak kullanmak veya destek almak için iletişime geçebilirsiniz. E-Posta adresim: **[mefeocal455@gmail.com](mailto:mefeocal455@gmail.com)**
