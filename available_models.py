import google.generativeai as genai
genai.configure(api_key="AIzaSyAPNqBA-Y0JNVdAZLB5sZoU7r14ZY1hCqU")
for model in genai.list_models():
    print(model.name, model.supported_generation_methods)
