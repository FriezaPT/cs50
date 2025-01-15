# Internal Kitchen orders and recipes organizer
### Video Demo:  <URL HERE>
### Description:
This app is designed to help small kitchen staff manage recipes and orders. It allows users to:

- Create a database of ingredients, recipes, and suppliers, all editable.
- Organize and store orders and order information.
- Store and print simple recipe pages.


The app requires user input for all steps. It prioritizes quick action, allowing users to add, edit, or remove ingredients and recipes with just a few clicks.

The app's visual design is intentionally minimal, allowing for customization to match the client's branding.

Future development may include integration with supplier APIs for dynamic ingredient lists.

# Most relevant paths:
## Adding a New Ingredient

1. **From the Dashboard:** Click on the "Ingredients" tab.
2. **Ingredient List:** This page displays your existing ingredients. Click the "Add New Ingredient" button.
3. **Ingredient Form:**  Fill out the form with the ingredient details.
4. **Save:** Click the "Add Ingredient" button to save the new ingredient to your database.

## Creating a New Recipe

1. **From the Dashboard:** Click on the "Recipes" tab.
2. **Recipe List:** This page shows your saved recipes. Click the "Add New Recipe" button.
3. **Recipe Form:**  Fill out the form with the recipe details.
4. **Save:** Click the "Add Recipe" button to save the new recipe.


## Creating a New Order

1. **From the Dashboard:** Click on the "Orders" tab.
2. **Order List:** This page displays your current and past orders. Click the "New Order" button.
3. **Order Form:**
    * **Select Ingredients:** Begin typing the name of an ingredient. The app will suggest matches from your database.
        * Select the ingredient you need.
        * Enter the quantity required for this order.
        * Repeat for all ingredients needed.
4. **Confirm Order:** Review your order and click the "Confirm Order" button to place the order.

## Creating an Order from Recipes

This method allows you to quickly generate an order based on your existing recipes.

1. **From the Dashboard:** Click on the "Recipes" tab.
2. **Recipe List:** This page shows all your saved recipes.
    * **Select Recipes:** Check the box next to each recipe you want to include in your order.
3. **Adjust Quantities:**
    * **Multiplier:** For each selected recipe, enter a multiplier to adjust the ingredient quantities.
        * For example, if a recipe yields 4 servings and you need 8 servings, enter a multiplier of "2".
4. **"Order Recipes" Button:** Click this button to generate an order based on your selected recipes and multipliers.
5. **Order Review:**
    * **Edit Order:**
        * Add or remove ingredients as needed.
        * Adjust quantities further if required.
6. **Confirm Order:**  Review the final order and click "Confirm Order" to place it.

## Important Notes:

* **Allergens and Units:** Please note that the list of allergens and unit options are currently hard-coded within the app.
