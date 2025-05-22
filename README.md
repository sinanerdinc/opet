[![Python CI Workflow Status](https://github.com/sinanerdinc/opet/actions/workflows/ci.yml/badge.svg)](https://github.com/sinanerdinc/opet/actions/workflows/ci.yml)

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

## Testing
Bu proje, kod kalitesini ve güvenilirliğini sağlamak amacıyla `pytest` kullanılarak yazılmış birim testleri içermektedir. Testler, kodda yapılan her değişiklikte ve `main` branch'ine yapılan pull request'lerde GitHub Actions aracılığıyla otomatik olarak çalıştırılır. Bu sayede projenin istikrarlı bir şekilde geliştirilmesi hedeflenmektedir.

## Docker
Uygulamayı docker üzerinden kullanabilirsiniz. İsterseniz Dockerfile üzerinden şu komut ile kendiniz bir build alabilirsiniz.
```
docker build -t opet .
```

isterseniz de [dockerhub üzerindeki imajı](https://hub.docker.com/r/sinanerdinc/opet) kullanabilirsiniz.

```
docker pull sinanerdinc/opet
```