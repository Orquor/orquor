import urllib.request, json, random, string

# Generar contraseña
chars = string.ascii_letters + string.digits + "!@#$%&*"
pwd = ''.join(random.choice(chars) for _ in range(16))

# Usar la API de X no es posible sin cuenta. Mejor ir vía navegador.
# Por ahora guardamos la contraseña generada
with open(r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\credenciales.txt", "a") as f:
    f.write(f"\nX/Twitter @orquor (NUEVA): freddy@orquor.com | {pwd}\n")

print(f"X password: {pwd}")
print("Abre https://x.com/i/flow/signup para crear la cuenta.")
print(f"Email: freddy@orquor.com")
print(f"Handle deseado: @orquor")
print(f"Nombre: Orquor")
