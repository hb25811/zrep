import streamlit as st
from openai import OpenAI

client = OpenAI(api_key='')


# Function for text generation
def get_job_info(job_title):
    prompt = f"What are the technical and soft skills required for the role of {job_title}?"
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def get_degree_certificates(job_title):
    prompt = f"What degrees or certifications are required for the role of {job_title}?"
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

# Function for image generation
def generate_image(job_title):
    prompt = f"A typical workspace for a {job_title}."
    response = client.images.generate(prompt=prompt,
    n=1,
    size="1024x1024")
    return response.data[0].url

# Streamlit UI
st.title("Avee Patel's Career Exploration Tool!")
st.write("Explore various careers by entering a job title.")

job_title = st.text_input("Enter the job title:")
if st.button("Get Information"):
    if job_title:
        job_info = get_job_info(job_title)
        degree_info = get_degree_certificates(job_title)

        st.subheader("Job Information")
        st.write(job_info)

        st.subheader("Required Degrees/Certificates")
        st.write(degree_info)

        image_url = generate_image(job_title)
        st.image(image_url, caption=f"Workspace for a {job_title}", use_column_width=True)
    else:
        st.error("Please enter a job title.")
