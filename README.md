## HaUI-Admission-Chatbot

## 📌 Introduction
An intelligent chatbot system designed to assist with admission inquiries for Hanoi University of Industry (HaUI). The chatbot leverages RAG (Retrieval-Augmented Generation) architecture to provide accurate and context-aware responses about admission information.

## 🚀 Key Features
- Real-time admission information retrieval
- Natural language query understanding
- Context-aware responses
- Support FAQ
- Understand complex table structures (auto detect merged column, auto detect table with complex structure,...)
- Multilingual support (Vietnamese/English)
- Conversation history tracking
- REST API endpoints

## 🛠 Technologies
- **Backend**: Python, FastAPI
- **LLM Integration**: LangChain
- **Vector Database**: Qdrant
- **Containerization**: Docker
- **API Documentation**: Swagger/OpenAPI
- **Models**: OpenAI GPT models

## 🔧 Installation & Setup
1. Clone the repository:
```bash
git clone https://github.com/tngphmvan/HaUI-Admission-Chatbot.git
cd app
```
2. Set up environment variables:
```bash
cp .env.example .env
# Add your OpenAI API key and other configurations
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --reload --log-level debug -- workers 4
```
5. Access the API documentation at `http://localhost:8000/docs`.

## 🔥 Docker Deployment
1. Build the Docker image:
```bash
docker build -t haui-chatbot .
```
2. Run the Docker container:
```bash
docker run -d -p 8000:8000 haui-chatbot
```
3. Access the API documentation at `http://localhost:8000/docs`.

## 🎯 Usage Guide
1. API endpoints available at http://localhost:8000/docs
2. Send queries via REST API
3. View conversation history and responses
4. Send a POST request to `/chatbot` with the following payload:
```json
{
  "message": "What are the admission requirements for Computer Science?"
}
```
## 🏗 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
