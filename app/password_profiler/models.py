from collections import Counter
import string
import math
import os
import hashlib

from dotenv import load_dotenv

load_dotenv()


COMM_PASS_LIST = os.getenv('COMMONS_PATH')
HASH_ALGO = os.getenv("HASH_ALGO")
FREQUENCY_THRESHHOLD = 20

class StrengthChecker:
    def __init__(self, password: str) -> None:
        self.score = 0
        self.password = password
        self.classification = "None"

    def char_type_check(self) -> list:
        """
        checks whether password has upper, lower, special chars and/or digits within its string
        """
        upper_case = any([1 if c in string.ascii_uppercase else 0 for c in self.password])
        lower_case = any([1 if c in string.ascii_lowercase else 0 for c in self.password])
        special = any([1 if c in string.punctuation else 0 for c in self.password])
        digits = any([1 if c in string.digits else 0 for c in self.password])

        self.chars = [upper_case, lower_case, special, digits]
        if all(self.chars):
            self.score += 1

        return self.chars

    def check_commons(self) -> bool:
        """
        check if password in common password list (rockyou.txt)
        """
        with open(COMM_PASS_LIST) as f:
            common = f.read().splitlines()

        if self.password in common:
            self.score = 0
            return True
        else:
            self.score += 1
            return False
            
    def calculate_entropy(self, char_string: str) -> float:
        """
        calculates entropy of characters within the string
        """
        # Count the occurrences of each character in the string
        counts = Counter(char_string)
        
        # Calculate the probability of each character
        total_elements = len(char_string)
        probabilities = [count / total_elements for count in counts.values()]
        
        # Calculate entropy using the formula: -p * log2(p)
        self.entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        return self.entropy
    
    # high frequency characters profiling
    
    def hash_string(self, input_string) -> str:
        """
        converts input string hash into its hexadecimal representation
        """
        # init hashlib object
        hasher_obj = hashlib.new(HASH_ALGO)
        # update the hashlib object with the input string encoded as bytes
        hasher_obj.update(input_string.encode())
        # return the hexadecimal representation of the hash
        return hasher_obj.hexdigest()

    def count_char_occurrences(self, input_string):
        """
        counts occurences of characters within input_string
        """
        char_count = {}
        total_chars = len(input_string)

        for char in input_string:
            hex_char_hash = self.hash_string(char)
            if hex_char_hash not in char_count:
                char_count[hex_char_hash] = 0
            char_count[hex_char_hash] += 1

        return char_count, total_chars

    def calculate_relative_percentages(self, char_count, total_chars) -> dict:
        relative_percentages = {}
        for hex_char, count in char_count.items():
            relative_percentages[hex_char] = round((count / total_chars) * 100, 3)

        return relative_percentages

    def check_frequency(self) -> bool:
        # track high frequency character
        self.high_frequency = False
        char_count, total_chars = self.count_char_occurrences(self.password)
        self.relative_percentages = self.calculate_relative_percentages(char_count, total_chars)
        for _, percent in self.relative_percentages.items():
            # check threshold
            if percent > FREQUENCY_THRESHHOLD:
                self.high_frequency = True
        return self.high_frequency

    # scores
    
    def profile_score(self) -> int:
        # check password length
        if len(self.password) >= 8:
            self.score += 1
        if len(self.password) >= 16:
            self.score += 1
        if len(self.password) >= 24:
            self.score += 1
        # check character composition
        if sum(self.chars) > 2:
            self.score += 1
        if sum(self.chars) > 3:
            self.score += 1
        # check entropy
        if self.entropy > 3:
            self.score += 1
        # check high frequency
        if self.high_frequency:
            self.score -= 1 if self.score > 0 else 0
        else:
            self.score += 2
        
        return self.score

    def classify(self) -> None:
        if self.score == 0:
            self.classification = "very weak"
        elif 1 <= self.score < 4:
            self.classification = "weak"
        elif 4 <= self.score < 6:
            self.classification = "moderate"
        elif 6 <= self.score < 8:
            self.classification = "strong"
        elif self.score >= 8:
            self.classification = "very strong"
            
    def run(self) -> dict:
        self.char_type_check()

        common = self.check_commons()

        self.calculate_entropy(self.password)

        self.check_frequency()
        
        self.profile_score()

        self.classify()
        
        self.report = {
            "score": self.score, 
            "entropy": self.entropy, 
            "common": common, 
            "classification": self.classification, 
            "char_frequency": [self.relative_percentages, self.high_frequency]
            }
        
        return self.report
        
        