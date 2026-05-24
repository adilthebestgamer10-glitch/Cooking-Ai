#!/usr/bin/env python3
"""
Cooking AI - Your Personal Chef Assistant
Uses Google Gemini AI to create personalized recipes
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load environment variables
load_dotenv()

class CookingAI:
    def __init__(self):
        """Initialize the Cooking AI with Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print(f"{Fore.RED}❌ Error: GEMINI_API_KEY not found in .env file")
            print(f"{Fore.YELLOW}📝 Please create a .env file with your API key")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        print(f"{Fore.GREEN}✅ Cooking AI initialized successfully!\n")
    
    def create_recipe(self, food, budget=None, dietary_restrictions=None, difficulty="easy"):
        """
        Create a recipe based on user preferences
        
        Args:
            food: The dish the user wants to cook
            budget: Budget constraint (e.g., "$10")
            dietary_restrictions: List of restrictions (e.g., "vegetarian")
            difficulty: Difficulty level (easy, medium, hard)
        """
        
        # Build the prompt
        prompt = f"""
        You are an expert chef AI assistant. Create a detailed recipe with these requirements:
        
        DISH: {food}
        DIFFICULTY LEVEL: {difficulty}
        """
        
        if budget:
            prompt += f"BUDGET LIMIT: {budget}\nInclude approximate costs for each ingredient.\n"
        
        if dietary_restrictions:
            prompt += f"DIETARY RESTRICTIONS: {', '.join(dietary_restrictions)}\n"
        
        prompt += """
        IMPORTANT FORMATTING INSTRUCTIONS:
        1. Make the recipe VERY EASY to understand
        2. Use simple words (no fancy cooking terms unless explained)
        3. Break down each step clearly with numbers
        4. Explain WHY each step matters
        5. If budget mentioned, show total cost
        6. Include cooking tips for beginners
        7. Use emojis to make it fun and easy to read
        8. Format with clear sections:
           - 📋 INGREDIENTS
           - 💰 COST (if budget given)
           - 👨‍🍳 COOKING STEPS
           - 💡 BEGINNER TIPS
           - ⏱️ TIME & SERVINGS
        
        Remember: Make this so easy that even a 10-year-old can follow it!
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"{Fore.RED}❌ Error creating recipe: {str(e)}"
    
    def explain_ingredient(self, ingredient):
        """
        Explain what an ingredient does and why it's used
        """
        prompt = f"""
        Explain the ingredient '{ingredient}' in very simple terms:
        1. What it is (in simple words)
        2. Why we use it in cooking
        3. What it does to food
        4. Can it be replaced with anything?
        
        Use ONLY 2-3 sentences. Make it understandable for kids!
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"{Fore.RED}❌ Error: {str(e)}"
    
    def get_substitutions(self, ingredient):
        """
        Get healthy or budget-friendly substitutions for an ingredient
        """
        prompt = f"""
        Give me 3 substitutions for '{ingredient}':
        1. For budget (cheaper option)
        2. For health (healthier option)
        3. For allergies (alternative)
        
        Format each as: Substitution → Why it works
        Keep it simple!
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"{Fore.RED}❌ Error: {str(e)}"


def print_menu():
    """Display the main menu"""
    print(f"{Fore.CYAN}" + "="*50)
    print(f"{Fore.CYAN}🍳 WELCOME TO COOKING AI - Your Personal Chef!")
    print(f"{Fore.CYAN}" + "="*50)
    print(f"{Fore.GREEN}1. 🍕 Create a Recipe")
    print(f"{Fore.GREEN}2. 🔍 Explain an Ingredient")
    print(f"{Fore.GREEN}3. 💱 Find Substitutions")
    print(f"{Fore.GREEN}4. ❌ Exit")
    print(f"{Fore.CYAN}" + "="*50)


def get_recipe_input():
    """Get recipe preferences from user"""
    print(f"\n{Fore.YELLOW}📝 Let's create your recipe!\n")
    
    food = input(f"{Fore.CYAN}What do you want to cook? {Fore.WHITE}")
    
    budget_choice = input(f"{Fore.CYAN}Do you have a budget? (yes/no) {Fore.WHITE}").lower()
    budget = None
    if budget_choice == 'yes':
        budget = input(f"{Fore.CYAN}What's your budget? (e.g., $10, $20) {Fore.WHITE}")
    
    dietary_choice = input(f"{Fore.CYAN}Any dietary restrictions? (yes/no) {Fore.WHITE}").lower()
    dietary_restrictions = None
    if dietary_choice == 'yes':
        dietary_text = input(f"{Fore.CYAN}List them (e.g., vegetarian, gluten-free): {Fore.WHITE}")
        dietary_restrictions = [x.strip() for x in dietary_text.split(',')]
    
    difficulty = input(f"{Fore.CYAN}Difficulty level? (easy/medium/hard) [default: easy] {Fore.WHITE}") or "easy"
    
    return food, budget, dietary_restrictions, difficulty


def main():
    """Main application loop"""
    try:
        ai = CookingAI()
        
        while True:
            print_menu()
            choice = input(f"{Fore.YELLOW}Enter your choice (1-4): {Fore.WHITE}")
            
            if choice == '1':
                food, budget, dietary_restrictions, difficulty = get_recipe_input()
                print(f"\n{Fore.YELLOW}🧑‍🍳 Creating your recipe...\n")
                recipe = ai.create_recipe(food, budget, dietary_restrictions, difficulty)
                print(f"{Fore.GREEN}{recipe}")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            
            elif choice == '2':
                ingredient = input(f"{Fore.CYAN}What ingredient do you want to know about? {Fore.WHITE}")
                print(f"\n{Fore.YELLOW}🔍 Explaining...\n")
                explanation = ai.explain_ingredient(ingredient)
                print(f"{Fore.GREEN}{explanation}")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            
            elif choice == '3':
                ingredient = input(f"{Fore.CYAN}Which ingredient do you want to replace? {Fore.WHITE}")
                print(f"\n{Fore.YELLOW}💱 Finding substitutions...\n")
                substitutions = ai.get_substitutions(ingredient)
                print(f"{Fore.GREEN}{substitutions}")
                input(f"\n{Fore.CYAN}Press Enter to continue...")
            
            elif choice == '4':
                print(f"\n{Fore.CYAN}👋 Thanks for using Cooking AI! Happy cooking! 🍳\n")
                break
            
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please try again.\n")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}👋 Goodbye! Keep cooking! 🍳")
        sys.exit(0)


if __name__ == "__main__":
    main()
