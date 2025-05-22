import spacy
import nltk
import string

# Ensure NLTK resources are available (stopwords, punkt)
# These should have been downloaded during the setup phase.
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    print("NLTK stopwords not found. Please run: python -c \"import nltk; nltk.download('stopwords')\"")
    # As a fallback, define a minimal list or raise an error
    # For this script, we'll assume the calling environment handles NLTK downloads.

try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    print("NLTK punkt not found. Please run: python -c \"import nltk; nltk.download('punkt')\"")

# Load spaCy model
# This should have been downloaded during the setup phase (python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("SpaCy 'en_core_web_sm' model not found. Please run: python -m spacy download en_core_web_sm")
    # Fallback or error if spaCy model is critical and not found
    nlp = None  # Set to None if essential and not found, functions should handle this

# Get NLTK English stopwords
stop_words = set(nltk.corpus.stopwords.words('english'))

def lowercase_text(text):
    """Converts text to lowercase."""
    if not isinstance(text, str):
        return ""
    return text.lower()

def remove_punctuation(text):
    """Removes punctuation from text."""
    if not isinstance(text, str):
        return ""
    # Create a translation table: str.maketrans(from, to, delete_chars)
    # Here, we want to delete all characters found in string.punctuation
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_stopwords_nltk(text):
    """Removes NLTK stopwords from text."""
    if not isinstance(text, str):
        return ""
    words = nltk.tokenize.word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_words)

def lemmatize_text_spacy(text):
    """Lemmatizes text using spaCy."""
    if not isinstance(text, str):
        return ""
    if nlp is None:
        print("SpaCy nlp model not loaded. Skipping lemmatization.")
        return text  # Or raise an error
    
    doc = nlp(text)
    lemmatized_words = [token.lemma_ for token in doc]
    return " ".join(lemmatized_words)

def preprocess_text(text):
    """
    Applies a full preprocessing pipeline to the text:
    1. Lowercasing
    2. Punctuation removal
    3. Stopword removal (NLTK)
    4. Lemmatization (spaCy)
    """
    if not isinstance(text, str):
        print("Warning: preprocess_text received non-string input.")
        return ""
    
    text = lowercase_text(text)
    text = remove_punctuation(text)
    
    # Tokenization is implicit in NLTK's remove_stopwords and spaCy's lemmatization
    # If using custom tokenization before these steps, ensure it's compatible.
    text = remove_stopwords_nltk(text)  # NLTK tokenizes and joins
    
    if nlp:  # Proceed with spaCy only if model loaded
        text = lemmatize_text_spacy(text)  # spaCy processes and joins
    else:
        print("Skipping lemmatization as spaCy model is not available.")
    
    # Clean up extra whitespace that might have been introduced
    text = " ".join(text.split())
    
    return text

if __name__ == '__main__':
    sample_text = "Hello World! This is an example sentence for text preprocessing, showing off NLTK and spaCy capabilities. We'll see how it works."
    
    print("Original Text:")
    print(sample_text)
    print("-" * 30)
    
    lower_text = lowercase_text(sample_text)
    print("\nLowercased Text:")
    print(lower_text)
    print("-" * 30)
    
    no_punctuation_text = remove_punctuation(lower_text)
    print("\nText with Punctuation Removed:")
    print(no_punctuation_text)
    print("-" * 30)
    
    no_stopwords_text_nltk = remove_stopwords_nltk(no_punctuation_text)
    print("\nText with NLTK Stopwords Removed:")
    print(no_stopwords_text_nltk)
    print("-" * 30)
    
    if nlp:
        lemmatized_text_spacy = lemmatize_text_spacy(no_stopwords_text_nltk)  # Lemmatize the already stopword-removed text
        print("\nText after SpaCy Lemmatization (on NLTK stopword removed text):")
        print(lemmatized_text_spacy)
        print("-" * 30)
        
        # Test the full pipeline
        processed_text_pipeline = preprocess_text(sample_text)
        print("\nFully Preprocessed Text (Pipeline):")
        print(processed_text_pipeline)
        print("-" * 30)
    else:
        print("\nSkipping SpaCy lemmatization and full pipeline test as 'en_core_web_sm' model is not loaded.")
    
    # Example with a slightly different sentence
    another_sample = "Job descriptions often contain many specific skills like Python, Java, and Machine Learning."
    print("\nAnother Original Text:")
    print(another_sample)
    processed_another_sample = preprocess_text(another_sample)
    print("\nProcessed Another Text:")
    print(processed_another_sample)
    print("-" * 30)
    
    # Test edge cases
    empty_text = ""
    print("\nOriginal Text (Empty):")
    print(f"'{empty_text}'")
    processed_empty_text = preprocess_text(empty_text)
    print("\nProcessed Text (Empty):")
    print(f"'{processed_empty_text}'")
    print("-" * 30)
    
    text_with_numbers = "Experience required 5 years with version 2.0 of software."
    print("\nOriginal Text (with numbers):")
    print(text_with_numbers)
    processed_text_with_numbers = preprocess_text(text_with_numbers)
    print("\nProcessed Text (with numbers):")
    # Note: numbers are not explicitly removed by this pipeline
    print(processed_text_with_numbers)
    print("-" * 30)
    
    non_string_input = 12345
    print(f"\nOriginal Text (non-string): {non_string_input}")
    processed_non_string = preprocess_text(non_string_input)
    print(f"\nProcessed Text (non-string): '{processed_non_string}'")
    print("-" * 30)
