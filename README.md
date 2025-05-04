# FindPaw 🐾

**FindPaw** é um sistema inteligente de monitoramento e rastreamento de animais domésticos desaparecidos, utilizando serviços da **AWS** para reconhecimento facial, rastreamento via GPS e análise de dados em tempo real.

---

## 📌 **Objetivo**
O projeto visa reduzir o índice de abandono e perdas de animais domésticos, oferecendo uma solução integrada para identificação, localização e monitoramento de saúde dos pets.

---

## ⚙️ **Tecnologias Utilizadas**
FindPaw emprega serviços avançados da **AWS**, garantindo eficiência e escalabilidade:

- **AWS Cognito** – Autenticação segura dos usuários.
- **AWS API Gateway** – Acesso remoto aos dados.
- **Amazon S3** – Armazenamento de imagens de pets desaparecidos.
- **AWS Rekognition** – Reconhecimento facial para busca de animais.
- **Amazon DynamoDB** – Banco de dados NoSQL escalável.
- **Amazon Location Service** – Rastreamento via GPS.
- **Amazon SNS** – Envio de notificações aos tutores.
- **AWS Lambda** – Processamento automatizado de eventos.
- **Amazon CloudWatch** – Monitoramento e geração de logs.
- **Amazon Connect** – Alertas emergenciais para tutores.

---

## 🚀 **Instalação**
Para configurar o projeto **FindPaw** localmente, siga os passos:

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/findpaw.git
   cd findpaw
npm install
```
AWS_ACCESS_KEY_ID=xxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxx
```
npm start
```
```
📌 Uso
- Os tutores cadastram seus pets no sistema.
- O sistema realiza a identificação facial e registra no banco de dados.
- Em caso de desaparecimento, o usuário pode ativar o rastreamento por GPS.
- Notificações são enviadas a comunidades próximas para ajudar na busca.

📊 Estimativa de Custos
Conforme a AWS Pricing Calculator, os custos estimados para 12 meses são:
| Serviço | Mensal (USD) | Anual (USD) | 
| Amazon S3 | 0.21 | 2.52 | 
| AWS Lambda | 0.00 | 0.00 | 
| Amazon CloudWatch | 3.60 | 43.21 | 
| Amazon DynamoDB | 51.14 | 793.68 | 
| Amazon SNS | 245.48 | 2945.76 | 
| Amazon Location Service | 0.58 | 6.96 | 


🔗 Mais detalhes na estimativa oficial: AWS Pricing Calculator

🛠 Contribuições
Contribuições são bem-vindas! Para colaborar:
- Faça um fork do repositório.
- Crie uma branch com sua alteração:git checkout -b minha-alteracao

- Envie um Pull Request.


📄 Licença
Este projeto é licenciado sob a MIT License – veja o arquivo LICENSE para mais detalhes.


