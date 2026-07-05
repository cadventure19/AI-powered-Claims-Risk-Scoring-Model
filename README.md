    Repository Structure
    The repository consists of four core files:

    prediction_model.ipynb (Jupyter Notebook)

    The core machine learning pipeline. It includes data preprocessing, exploratory data analysis (EDA), model training, and performance evaluation. It is fully self-contained and ready to run out of the box once the dataset is loaded.

    llm_response_code.py

    The Generative AI component of the project. It hooks into the machine learning model's output to dynamically generate 2-line, layman-friendly risk summaries and operational next steps for claims auditors.

   model_document.docx

    A comprehensive business and technical brief containing detailed answers to project stakeholders regarding framework design, model trade-offs, data distributions, and future enhancements.

    prediction_current_claim.csv

    The final inference output containing risk scores, risk classifications, and structured data payloads for the target claims evaluated by the model.
