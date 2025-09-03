import string

def encrypt_character(ch, shift1, shift2):
    
    if ch.islower():
        if ch in "abcdefghijklmnopqrstuvwxyz":  
            shift = shift1 * shift2
            alphabet = string.ascii_lowercase
            return alphabet[(alphabet.index(ch) + shift) % 26]
        else: 
            shift = shift1 + shift2
            alphabet = string.ascii_lowercase
            return alphabet[(alphabet.index(ch) - shift) % 26]

   
    elif ch.isupper():
        if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":  
            shift = shift1
            alphabet = string.ascii_uppercase
            return alphabet[(alphabet.index(ch) - shift) % 26]
        else:  
            shift = shift2 ** 2
            alphabet = string.ascii_uppercase
            return alphabet[(alphabet.index(ch) + shift) % 26]

 
    else:
        return ch


def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    encrypted_text = "".join(encrypt_character(ch, shift1, shift2) for ch in raw_text)

    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted_text)


def decrypt_character(ch, shift1, shift2):
   
    if ch.islower():
        if ch in "abcdefghijklmnopqrstuvwxyz": 
            shift = shift1 * shift2
            alphabet = string.ascii_lowercase
            return alphabet[(alphabet.index(ch) - shift) % 26]
        else: 
            shift = shift1 + shift2
            alphabet = string.ascii_lowercase
            return alphabet[(alphabet.index(ch) + shift) % 26]

    elif ch.isupper():
        if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":  
            shift = shift1
            alphabet = string.ascii_uppercase
            return alphabet[(alphabet.index(ch) + shift) % 26]
        else:  
            shift = shift2 ** 2
            alphabet = string.ascii_uppercase
            return alphabet[(alphabet.index(ch) - shift) % 26]

    else:
        return ch


def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        encrypted_text = f.read()

    decrypted_text = "".join(decrypt_character(ch, shift1, shift2) for ch in encrypted_text)

    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted_text)


def verify():
    with open("raw_text.txt", "r", encoding="utf-8") as f1, open("decrypted_text.txt", "r", encoding="utf-8") as f2:
        raw = f1.read()
        decrypted = f2.read()

    if raw == decrypted:
        print("Decryption successful! Files match.")
    else:
        print("Decryption failed! Files do not match.")


def main():
    shift1 = int(input("Enter shift1 value: "))
    shift2 = int(input("Enter shift2 value: "))

    print("Encrypting the raw_text.txt file...")
    encrypt_file(shift1, shift2)

    print("Decrypting the encrypted_text.txt file...")
    decrypt_file(shift1, shift2)

    print("Verifying...")
    verify()


if __name__ == "__main__":
    main()
