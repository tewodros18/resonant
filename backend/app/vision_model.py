from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import torch

model = None
processor = None

def load_model():
    model_id = 'florence'
    global model
    global processor

    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval().cuda()
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
def run_example(task_prompt, text_input=None):
    if text_input is None:
        prompt = task_prompt
    else:
        prompt = task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt").to('cuda', torch.float32)
    generated_ids = model.generate(
      input_ids=inputs["input_ids"].cuda(),
      pixel_values=inputs["pixel_values"].cuda(),
      max_new_tokens=1024,
      early_stopping=False,
      do_sample=False,
      num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text, 
        task=task_prompt, 
        image_size=(image.width, image.height)
    )
    return parsed_answer
def get_caption_grounding(caption_input):
    task_prompt = '<CAPTION_TO_PHRASE_GROUNDING>'
    results = run_example(task_prompt, text_input=caption_input)
    return results

image = Image.open(r"./judith.jpg")



load_model()  

task_prompt = '<DENSE_REGION_CAPTION>'
results = run_example(task_prompt)
print(results)