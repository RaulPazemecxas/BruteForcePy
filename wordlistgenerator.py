# Gera combinações de letras minúsculas (a-z) e números (1-100)
wordlist = []
for letter in range(ord('a'), ord('z')+1):
    for number in range(1, 101):
        wordlist.append(f"{chr(letter)}{number}")

# Salva a wordlist em um arquivo de texto
with open("wordlist.txt", "w") as file:
    file.write("\n".join(wordlist))

print("Wordlist gerada com sucesso e salva em 'wordlist.txt'")
