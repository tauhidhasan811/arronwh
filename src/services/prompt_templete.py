from typing import List, Dict
from langchain_core.prompts import PromptTemplate
from langchain.messages import HumanMessage, SystemMessage

class PromptGenerator:
    MAX_HISTORY_ITEMS = 8

    @staticmethod
    def _compact_previous_chat(previous_chat: List[Dict]):
        if not previous_chat:
            return []

        compact_chat = []
        for item in previous_chat[-PromptGenerator.MAX_HISTORY_ITEMS:]:
            if hasattr(item, "model_dump"):
                item = item.model_dump()

            user_query = str(item.get("user_query", ""))[:500]
            ai_response = str(item.get("ai_response", ""))[:700]
            compact_chat.append({
                "user_query": user_query,
                "ai_response": ai_response,
            })

        return compact_chat

    @staticmethod
    def output_templete():
        # Fixed string formatting and removed unnecessary concatenation
        return (
            "Write like a friendly human chat assistant. Keep responses concise, helpful, and easy to scan. "
            "Use light, relevant emojis sparingly, such as 👍, when it feels natural. "
            "Use plain text for normal sentences. Do not wrap normal sentences in HTML tags. "
            "For greetings, use one warm short sentence and ask how you can help. "
            "For service questions, use a short intro sentence, then a <ul><li> list using only services found in RAG or tools data. "
            "For purchase, quote, or price questions, use a short intro sentence, then a <ul><li> step list. "
            "End helpful answers with one short follow-up question such as Was that helpful? or Is that what you were looking for? "
            "Always format phone numbers as <a href=\"tel:08001234567\">0800 123 4567</a> and email addresses as <a href=\"mailto:hello@yoloheat.co.uk\">hello@yoloheat.co.uk</a>. "
            "Only use these HTML tags: <ul>, <li>, and <a>. Do not use <p>, <table>, <tr>, <td>, <h1>, <h2>, <b>, <strong>, <br>, or any other HTML tag. "
        )

    @staticmethod   
    def GeneralPrompt(user_query, relevent_info, previous_chat: List[Dict], 
                      file_data: dict):
        compact_chat = PromptGenerator._compact_previous_chat(previous_chat)
        sys_message = SystemMessage(
            content=(
                "You are an assistant for a boiler company that sells boilers, boiler controllers, and related products. "
                "Your responsibility is to answer customer queries about these products and use available tools when necessary. "
                "Always prioritize the Current user query over previous chat. "
                "Use previous chat only as recent context; never let it override the latest user message. "
                "If previous chat contains quote-page guidance, treat it as stale unless the current user query explicitly asks for a quote, purchase, order, installation booking, view boilers/products/options, or a personalised estimate. "
                "Use RAG as supporting context only; do not copy irrelevant RAG text into the answer. "
                "if file data are there then response on it is not read able is_read false then tell to send the customer support to make a proper document. "
                "The company provides boiler services only. Do not add services unless they appear in RAG or tools data. "
                "Provide accurate, concise, and relevant answers that sound like a helpful person, not a script. "
                "Do not mention the quote page for general questions, contact questions, boiler/controller information, or support questions. "
                "Only mention the quote page when the user explicitly asks to get a quote, buy, purchase, order, book an installation, view boilers/products/options, or create a personalised estimate. "
                "When the quote page is relevant, provide this link once: <a href=\"https://arronwh-website.vercel.app/boilers/property-overview\" target=\"_blank\">Create your own quote</a>. "
                "For buy or purchase questions, explain that it is simple: create your own quote, answer a few questions, compare suitable boiler options, choose an installation date if available, then the support team will contact them after quote completion. "
                "For quote questions, explain that the user can get a personalised quote online by answering a few questions about their home, then the support team will contact them after completion. "
                "For price questions, first use available RAG or tools data to give product prices when available. If no reliable price is available, say prices depend on the home and selected boiler and invite them to create their own quote. Do not invent prices. "
                "If the user wants to view boilers, products, or personalised options, tell them to use the quote page because those options depend on their home details. "
                "For service questions, answer with a short intro sentence followed by a <ul> list of boiler services from RAG or tools data only. "
                "For contact questions, tell users they can call <a href=\"tel:08001234567\">0800 123 4567</a> or email <a href=\"mailto:hello@yoloheat.co.uk\">hello@yoloheat.co.uk</a>. "
                "If the user has completed a quote or asks what happens after completing a quote, explain that the support team will contact them. "
                # "text will be short do not describe so long."
                "Do not hallucinate or make up information. "
                "If the question is outside the scope of boilers, boiler controllers, or related products, politely respond with a brief apology and state that you can only assist with company-related products. "
                f"follow this template {PromptGenerator.output_templete()}"
            )
        )

        hum_message = HumanMessage(
            content=(
                f'Current user query - answer this now: {user_query} '
                f"File Data : {file_data}"
                f'\n\nRelevant information from RAG: {relevent_info} '
                f'\n\nRecent chat context only: {compact_chat}'
            )
        )
        
        temp = PromptTemplate(template="System instruction: {sys_message}\n{hum_message}",
                             input_variables=['sys_message', 'hum_message'])
        
        prompt = temp.invoke(
            {
                'sys_message': sys_message.content,
                'hum_message': hum_message.content
            }
        )
        return str(prompt)

    @staticmethod   
    def ToolsPrompt(user_query, tools_data: List[Dict]):
        sys_message = SystemMessage(
            content=(
                "You are an assistant of the boiler company. "
                "Your task is to answer the current user query using only relevant tools data. "
                "The company provides boiler services only. Do not add services unless they appear in tools data. "
                "Do not mention the quote page unless the current user query explicitly asks for a quote, purchase, order, installation booking, view boilers/products/options, or a personalised estimate. "
                "When the quote page is relevant, use this link text: <a href=\"https://arronwh-website.vercel.app/boilers/property-overview\" target=\"_blank\">Create your own quote</a>. "
                "For service questions, answer with a short intro sentence followed by a <ul> list using only tools data. "
                "For purchase, quote, or view-product questions, answer with a short intro and a <ul> step list. "
                "For price questions, give prices from tools data when available. If no reliable price is available, invite the user to create their own quote. Do not invent prices. "
                "Always format phone numbers as <a href=\"tel:08001234567\">0800 123 4567</a> and email addresses as <a href=\"mailto:hello@yoloheat.co.uk\">hello@yoloheat.co.uk</a>. "
                # "text will be short do not describe so long."
                f"follow this template {PromptGenerator.output_templete()}"
            )
        )

        hum_message = HumanMessage(
            content=f'Current user Query: {user_query} \n\nTools data: {tools_data}'
        )
        
        temp = PromptTemplate(template="System instruction: {sys_message}\n{hum_message}",
                             input_variables=['sys_message', 'hum_message'])
        
        prompt = temp.invoke(
            {
                'sys_message': sys_message.content,
                'hum_message': hum_message.content
            }
        )
        return str(prompt)
