## Opet
Güncel yakıt fiyatlarını https://www.opet.com.tr/ üzerinden almanıza sağlar.

## Kullanım
Aşağıdaki komut ile paketi kurabilirsiniz.
```
pip install opet
```

Projeyi isterseniz aşağıdaki şekilde bir kütüphane olarak kullanabilirsiniz, veya opet-cli üzerinden terminalden kullanabilirsiniz.

```
client = OpetApiClient()

print(client.get_provinces())
print(client.get_districts(28))
print(client.get_price("028002"))
```

### get_provinces
Sistemde yakıt fiyatlarını çekmek için kullanabileceğiniz il ve kodlarını getirir.

### get_districts
Parametre olarak vereceğiniz il kodu sonrasında o ildeki ilçeleri getirir.

### get_price
Parametre olarak vereceğiniz ilçe kodu ile o ilçedeki yakıt fiyatlarına ulaşabilirsiniz.

## opet-cli
Terminal üzerinden plaka kodu parametresi geçerek yakıt fiyatlarını json formatında görebilirsiniz.

```
opet-cli --il 34
```