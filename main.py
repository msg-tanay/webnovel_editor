# # import google.generativeai as genai
# import os
from scraper import scrape,get_story,find_next, save_pdf, prepare_pdf, add_chapter_to_pdf

# # genai.configure(api_key=os.environ["GEMINI_NOVEL_EDITOR_API_KEY"])

# # model = genai.GenerativeModel("gemini-1.5-flash")

link='https://novelfull.com/monarch-of-evernight/chapter-1-crimson-colored-night.html'

story=get_story(scrape(link))
# # prompt=f"In the following text there are many grammatical, semantical and contextual errors. Correct those errors. Some of the errors will be in the form of mistaken pronouns, name change etc. This is the text that you need to work on {story}. Don't highlight the changes."

# # response = model.generate_content(prompt)
# # print(response.text)

save_pdf(link, "monarch_of_evernight.pdf")
