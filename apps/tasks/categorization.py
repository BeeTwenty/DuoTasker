import math
import re
import unicodedata


class CategoryResolver:
    def resolve(self, title, categories):
        raise NotImplementedError


class RulesCategoryResolver(CategoryResolver):
    _word_pattern = re.compile(r"[a-z0-9]+")
    _character_map = str.maketrans({
        "ø": "o",
        "æ": "ae",
        "å": "a",
        "ö": "o",
        "ä": "a",
        "ü": "u",
    })

    @classmethod
    def _clean_text(cls, value):
        normalized = unicodedata.normalize("NFKD", (value or "").casefold().translate(cls._character_map))
        return "".join(character for character in normalized if not unicodedata.combining(character)).strip()

    @classmethod
    def _word_set(cls, value):
        return set(cls._word_pattern.findall(cls._clean_text(value)))

    @classmethod
    def _keywords(cls, category):
        raw_keywords = category.keywords or ""
        return [keyword.strip() for keyword in raw_keywords.split(",") if keyword.strip()]

    @classmethod
    def _score(cls, title, keyword, category):
        normalized_title = cls._clean_text(title)
        normalized_keyword = cls._clean_text(keyword)
        if not normalized_title or not normalized_keyword:
            return 0

        if normalized_title == normalized_keyword:
            return 1000

        title_words = cls._word_set(normalized_title)
        keyword_words = cls._word_set(normalized_keyword)
        if not title_words or not keyword_words:
            return 0

        if normalized_keyword in normalized_title:
            return 500 + len(keyword_words)

        overlap = len(title_words & keyword_words)
        if overlap == 0:
            return 0

        if overlap == len(keyword_words):
            return 250 + overlap

        score = overlap * 10
        if category.is_important:
            score += 1
        return score

    def resolve(self, title, categories):
        best_category = None
        best_score = 0

        for category in categories:
            for keyword in self._keywords(category):
                score = self._score(title, keyword, category)
                if score > best_score:
                    best_score = score
                    best_category = category

        return best_category


class StatisticalCategoryResolver(CategoryResolver):
    """A lightweight built-in classifier using token frequencies over learned examples."""

    @staticmethod
    def _iter_training_texts(category):
        yield category.name
        for keyword in RulesCategoryResolver._keywords(category):
            yield keyword
        for task in category.tasks.all():
            yield task.title

    @classmethod
    def _tokens(cls, text):
        normalized = RulesCategoryResolver._clean_text(text)
        if not normalized:
            return []

        words = list(RulesCategoryResolver._word_pattern.findall(normalized))
        compact = normalized.replace(" ", "")
        ngrams = [compact[index : index + 3] for index in range(max(len(compact) - 2, 0))]
        return words + ngrams

    @classmethod
    def _category_model(cls, category):
        token_counts = {}
        total_tokens = 0
        sample_count = 0

        for text in cls._iter_training_texts(category):
            tokens = cls._tokens(text)
            if not tokens:
                continue
            sample_count += 1
            for token in tokens:
                token_counts[token] = token_counts.get(token, 0) + 1
                total_tokens += 1

        return token_counts, total_tokens, sample_count

    @classmethod
    def _score(cls, title_tokens, token_counts, total_tokens, sample_count, vocabulary_size):
        if not title_tokens or total_tokens == 0 or sample_count == 0:
            return float("-inf")

        score = math.log(sample_count)
        denominator = total_tokens + vocabulary_size
        for token in title_tokens:
            score += math.log((token_counts.get(token, 0) + 1) / denominator)
        return score

    def resolve(self, title, categories):
        category_models = []
        vocabulary = set()

        for category in categories:
            token_counts, total_tokens, sample_count = self._category_model(category)
            category_models.append((category, token_counts, total_tokens, sample_count))
            vocabulary.update(token_counts.keys())

        title_tokens = self._tokens(title)
        if not title_tokens or not vocabulary:
            return None

        vocabulary_size = max(len(vocabulary), 1)
        best_category = None
        best_score = float("-inf")

        for category, token_counts, total_tokens, sample_count in category_models:
            score = self._score(title_tokens, token_counts, total_tokens, sample_count, vocabulary_size)
            if score > best_score:
                best_score = score
                best_category = category

        return best_category


def resolve_category(title, categories):
    category_list = list(categories)
    rules_match = RulesCategoryResolver().resolve(title, category_list)
    if rules_match is not None:
        return rules_match

    return StatisticalCategoryResolver().resolve(title, category_list)