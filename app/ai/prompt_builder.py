from abc import ABC, abstractmethod


class PromptBuilder(ABC):

    @abstractmethod
    def build(self,*args,**kwargs,) -> tuple[str, str]:
        """
        Returns:
            (system_prompt, user_prompt)
        """
        pass


