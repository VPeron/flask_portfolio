from collections import Counter
import string
import math
import os

from dotenv import load_dotenv

load_dotenv()


COMM_PASS_LIST = os.getenv('COMMONS_PATH')


class StrengthChecker:
    def __init__(self, password: str) -> None:
        self.score = 0
        self.password = password
        self.classification = "None"
        #logger.info(f"Target: {self.password}")

    def char_type_check(self) -> list:
        # checks whether password has upper, lower, special chars and/or digits within its string
        upper_case = any([1 if c in string.ascii_uppercase else 0 for c in self.password])
        lower_case = any([1 if c in string.ascii_lowercase else 0 for c in self.password])
        special = any([1 if c in string.punctuation else 0 for c in self.password])
        digits = any([1 if c in string.digits else 0 for c in self.password])

        self.chars = [upper_case, lower_case, special, digits]
        #logger.info(f"Character Types met: {sum(self.chars)}")
        if all(self.chars):
            self.score += 1

        return self.chars

    def check_commons(self) -> bool:
        # check if password in common password list (rockyou.txt)
        with open(COMM_PASS_LIST) as f:
            common = f.read().splitlines()

        if self.password in common:
            #logger.info(f"Commons : True")
            self.score = 0
            return True
        else:
            #logger.info("Commons : False")
            self.score += 1
            return False
            
    def calculate_entropy(self, char_string: str) -> float:
        # Count the occurrences of each character in the string
        counts = Counter(char_string)
        
        # Calculate the probability of each character
        total_elements = len(char_string)
        probabilities = [count / total_elements for count in counts.values()]
        
        # Calculate entropy using the formula: -p * log2(p)
        self.entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
        #logger.info(f"Entropy score: {self.entropy}")
        return self.entropy

    def profile_length(self) -> int:
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

        return self.score

    def classify(self) -> None:
        #logger.info(f"Total score: {self.score}")
        if self.score == 0:
            #logger.info("Class: very weak")
            self.classification = "very weak"
        elif 1 <= self.score < 4:
            #logger.info("Class: weak")
            self.classification = "weak"
        elif 4 <= self.score < 6:
            #logger.info("Class: moderate")
            self.classification = "moderate"
        elif 6 <= self.score < 8:
            #logger.info("Class: strong")
            self.classification = "strong"
        elif self.score >= 8:
            #logger.info("Class: very strong")
            self.classification = "very strong"
        #logger.info("")
            
    def run(self) -> None:
        self.char_type_check()

        common = self.check_commons()

        self.calculate_entropy(self.password)

        self.profile_length()

        self.classify()
        
        self.report = {"score": self.score, "entropy": self.entropy, "common": common, "classification": self.classification}
        return self.report
        
        