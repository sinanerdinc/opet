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
print(client.get_price("55"))
```
### get_last_update
En son güncellemenin ne zaman olduğunu görebilirsiniz.

### get_provinces
Sistemde yakıt fiyatlarını çekmek için kullanabileceğiniz il ve kodlarını getirir.

### price
Parametre olarak vereceğiniz il kodu ile o ildeki yakıt fiyatlarına ulaşabilirsiniz.

## opet-cli
Terminal üzerinden plaka kodu parametresi geçerek yakıt fiyatlarını json formatında görebilirsiniz.

```
opet-cli --il 34
```

## Docker
Uygulamayı docker üzerinden kullanabilirsiniz. İsterseniz Dockerfile üzerinden şu komut ile kendiniz bir build alabilirsiniz.
```
docker build -t opet .
```

isterseniz de [dockerhub üzerindeki imajı](https://hub.docker.com/r/sinanerdinc/opet) kullanabilirsiniz.

```
docker pull sinanerdinc/opet
```