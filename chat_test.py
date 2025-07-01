from agent_logic import analizar_mensaje
from session_store import reset_session

def chat_loop():
    user_id = "usuario_terminal"
    reset_session(user_id)

    print(" Bienvenido al generador de contratos. Escribe tu solicitud.")

    while True:
        entrada = input(" Usuario: ")
        
        if entrada.lower() in ["salir", "exit", "cancelar", " "]:
            print("¡Si necesitas generar otro contra")
            break

        respuesta = analizar_mensaje(user_id, entrada)
        print(f"=> SAM: {respuesta}")

chat_loop()
