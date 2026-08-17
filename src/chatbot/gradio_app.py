import gradio as gr
import pandas as pd

from src.chatbot.recommendation_service import ChatbotRecommendationService
from src.recommendation.sentiment_data_loader import SentimentDataLoader


def create_app(data: pd.DataFrame | None = None) -> gr.Blocks:
    """Cria a interface Gradio do chatbot."""
    if data is None:
        data = SentimentDataLoader().load()

    service = ChatbotRecommendationService(data)

    with gr.Blocks(title="Playcatch") as demo:
        gr.Markdown(
            """
            # 🎵 Playcatch

            ### Recomendação musical por sentimento

            Diga como você está se sentindo ou que tipo de música deseja.
            """
        )

        query_input = gr.Textbox(
            label="O que você quer ouvir?",
            placeholder="Ex.: Quero músicas felizes",
            lines=2,
        )

        submit_button = gr.Button("Recomendar", variant="primary")

        response_output = gr.Textbox(
            label="Recomendações",
            lines=8,
            interactive=False,
        )

        submit_button.click(
            fn=service.handle_query,
            inputs=query_input,
            outputs=response_output,
        )

        query_input.submit(
            fn=service.handle_query,
            inputs=query_input,
            outputs=response_output,
        )

    return demo


def main() -> None:
    """Inicia a aplicação Gradio."""
    app = create_app()
    app.launch()


if __name__ == "__main__":
    main()
