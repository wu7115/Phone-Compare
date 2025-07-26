from flask import render_template, Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest
from comparer.data_ingestion import DataIngestor
from comparer.multi_agent_phone_system import LangGraphPhoneSystem
from langchain_groq import ChatGroq
from comparer.config import Config
from dotenv import load_dotenv
import time

load_dotenv()

# Custom metrics for Prometheus
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests") 
RESPONSE_COUNT = Counter("model_response_total", "Total Model Responses")
RESPONSE_LATENCY = Histogram("model_response_latency_seconds", "Model Response Latency in seconds")
OUT_OF_DOMAIN_COUNT = Counter("out_of_domain_queries_total", "Total Out-of-Domain Queries")
RESPONSE_TIME = Histogram("http_request_duration_seconds", "HTTP Request Duration")

def create_app():
    app = Flask(__name__)

    vector_store = DataIngestor().ingest(load_existing=True)
    multi_agent_system = LangGraphPhoneSystem(vector_store)

    @app.route("/")
    def index():
        REQUEST_COUNT.inc() # Each time hits the home page, REQUEST_COUNT increase by 1
        return render_template("index.html")
    
    @app.route("/get", methods=['POST'])
    def get_response():
        start_time = time.time()
        user_input = request.form["msg"]

        model_start_time = time.time()

        response, is_ood = multi_agent_system.process_query(user_input, session_id="user-session")
        
        model_end_time = time.time()

        if is_ood:
            OUT_OF_DOMAIN_COUNT.inc()

        RESPONSE_LATENCY.observe(model_end_time - model_start_time)
        RESPONSE_COUNT.inc()

        total_time = time.time() - start_time
        RESPONSE_TIME.observe(total_time)

        return response
    
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain") # Gives al the built-in metrics by Prometheus
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)