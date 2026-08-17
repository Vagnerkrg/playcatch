import gradio as gr
import pandas as pd

from src.app.playcatch_app import PlaycatchApp


def create_unified_app(
    data: pd.DataFrame | None = None,
) -> gr.Blocks:
    """Cria a interface unificada do Playcatch."""
    app = PlaycatchApp.from_csv() if data is None else PlaycatchApp(data)

    with gr.Blocks(title="Playcatch") as demo:
        gr.Markdown(
            """
            # 🎵 Playcatch

            ### Seu recomendador musical por sentimento

            Diga como você está se sentindo ou o que gostaria de ouvir.
            """
        )

        with gr.Row():
            query_input = gr.Textbox(
                label="O que você quer ouvir?",
                placeholder="Ex.: Quero músicas felizes",
                lines=2,
                scale=4,
            )

            submit_button = gr.Button(
                "Recomendar",
                variant="primary",
                scale=1,
            )

        current_emotion = gr.Textbox(
            label="Sentimento identificado",
            interactive=False,
        )

        response_output = gr.Textbox(
            label="Recomendações",
            lines=10,
            interactive=False,
        )

        def process_query(query: str) -> tuple[str, str]:
            """Processa a consulta e atualiza emoção e resposta."""
            response = app.recommend(query)

            emotion = app.chatbot.context.get_emotion()

            return emotion or "", response

        submit_button.click(
            fn=process_query,
            inputs=query_input,
            outputs=[current_emotion, response_output],
        )

        query_input.submit(
            fn=process_query,
            inputs=query_input,
            outputs=[current_emotion, response_output],
        )

        gr.Markdown(
            """
            ---
            **Contexto:** consultas como "quero mais parecidas" reutilizam
            o último sentimento identificado.
            """
        )

    return demo


def main() -> None:
    """Inicia a interface unificada."""
    app = create_unified_app()
    app.launch()


if __name__ == "__main__":
    main()
