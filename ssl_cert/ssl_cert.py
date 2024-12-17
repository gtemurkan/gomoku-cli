import subprocess
import os

def generate_ssl_cert(cert_file="server.crt", key_file="server.key"):
    """
    Генерирует самоподписанный SSL-сертификат и ключ.
    """
    # Проверяем, существуют ли уже файлы
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"Сертификат {cert_file} и ключ {key_file} уже существуют.")
        return

    # Команда для создания сертификата
    command = [
        "openssl", "req", "-new", "-x509", "-days", "365", "-nodes",
        "-out", cert_file,
        "-keyout", key_file,
        "-subj", "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
    ]

    try:
        # Выполняем команду
        subprocess.run(command, check=True)
        print(f"Сертификат создан: {cert_file}")
        print(f"Ключ создан: {key_file}")
    except FileNotFoundError:
        print("OpenSSL не найден. Убедитесь, что OpenSSL установлен и доступен в PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании сертификата: {e}")

if __name__ == "__main__":
    generate_ssl_cert()
