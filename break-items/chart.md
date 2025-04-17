# Items that cannot be crafted

- (1) Mild Herbs
- (2) Beast Meat
- (3) Tasty Wild Greens
- (4) Fresh Milk
- (5) Sleepy Cliff Salt
- (6) Fresh-Looking Egg
- (7) Colorful Berries
- (8) Golden Grains
- (26) Sweet & Fragrant Pressed Violets

# Items that are not used for crafting

- (20) Royal Fruit Ensemble
- (25) Soft Grilled Honey Mustard Chicken
- (30) Fruit-Nut-Cheese-Salami-Honey Bonanza
- (32) Super-Fresh Ham Saltimbocca
- (34) Huge Ratatouille Variety Quiche
- (38) Select Herbs & Melty Oxtail Soup
- (40) Fresh Variety Salad with Remoulade
- (44) Fromage Frais Gateau
- (48) Brioche French Toast
- (52) Eggs Benedict
- (56) Fluffy Lemon-Honey-Mint Souffle
- (58) Meat-Fish-Veggie Ajillo
- (62) Mango Bouquet
- (64) Queen Pineapple Parfait
- (68) Thick Cheese & Honey Apple Pie
- (72) Extra-Fruity Bircher Muesli
- (74) Fresh Veggie & Berry Yogurt Smoothie
- (76) Berry-Cinnamon Sangria
- (78) High-Grade Fruit Brandy
- (80) Mellow Aged Fermented Butter

# The full recipe chart, GL reading it

Highly recommend just copying the source and pasting it on Mermaid Live playground, then choose Adaptive display

```mermaid
---
config:
  theme: redux-dark
  look: classic
  layout: elk
---
flowchart TB
    subgraph Uncraftable
        B1["Mild Herbs"]
        B2["Beast Meat"]
        B3["Tasty Wild Greens"]
        B4["Fresh Milk"]
        B5["Sleepy Cliff Salt"]
        B6["Fresh-Looking Egg"]
        B7["Colorful Berries"]
        B8["Golden Grains"]
        B26["Sweet & Fragrant Pressed Violets"]
    end

    subgraph FirstOrder
        B9[Apple Mint Tea]
        B15[Sunny Apples]
        B21[Hearty Salted Steak]
        B27[Bottled Honey]
        B35[Fancy Veggie Hors D'oeuvres]
        B41[Homemade Cheese]
        B45[Rye Bread]
        B49[Invigorating Fried Eggs]
        B53[Fluffy Pancakes]
        B69[Roasted Mixed Nuts]
        B79["Smooth Butter"]
    end

    B1 -- x4 --> B9

    B1 -- x1 --> B15
    B7 -- x2 --> B15
    B8 -- x1 --> B15

    B2 -- x5 --> B21
    B5 -- x2 --> B21

    B4 -- x2 --> B27
    B5 -- x1 --> B27
    B7 -- x1 --> B27

    B1 -- x2 --> B35
    B3 -- x4 --> B35
    B5 -- x2 --> B35

    B2 -- x1 --> B41
    B4 -- x1 --> B41
    B5 -- x1 --> B41
    B6 -- x1 --> B41

    B3 -- x1 --> B45
    B4 -- x1 --> B45
    B8 -- x2 --> B45

    B5 -- x2 --> B49
    B6 -- x2 --> B49

    B4 -- x2 --> B53
    B6 -- x2 --> B53

    B8 -- x3 --> B69
    B5 -- x2 --> B69
    B3 -- x1 --> B69

    B4 -- x3 --> B79
    B5 -- x2 --> B79
    B6 -- x3 --> B79

    subgraph SecondOrder
        B10[Relaxing Honey Lemon Tea]
        B16[Fruit Punch]
        B28[Honey-Pickled Berries]
        B31[Sage-Wrapped Beast Meat]
        B33[Modest Quiche Lorraine]
        B37[Warm Onion Consomme]
        B39[Bagna Freida]
        B42[Thick Sour Yogurt]
        B46[Ham & Egg Sandwich]
        B50[Sun Bread]
        B54[Refreshing Berry Pancakes]
        B65[Pain Aux Frui]
        B70[Simple Granola]
        B73[Pulpy Berry Juice]
    end

    B9 -- x2 --> B10
    B27 -- x1 --> B10

    B15 -- x2 --> B16
    B1 -- x1 --> B16
    B4 -- x1 --> B16
    B7 -- x2 --> B16

    B27 -- x2 --> B28
    B15 -- x1 --> B28

    B21 -- x1 --> B31
    B1 -- x2 --> B31

    B45 -- x1 --> B33
    B2 -- x2 --> B33
    B6 -- x2 --> B33

    B3 -- x3 --> B37
    B5 -- x1 --> B37
    B41 -- x1 --> B37

    B1 -- x1 --> B39
    B3 -- x1 --> B39
    B5 -- x2 --> B39
    B41 -- x1 --> B39

    B41 -- x1 --> B42
    B79 -- x1 --> B42

    B45 -- x2 --> B46
    B49 -- x1 --> B46

    B49 -- x2 --> B50
    B45 -- x1 --> B50

    B53 -- x2 --> B54
    B7 -- x3 --> B54
    B1 -- x1 --> B54

    B45 -- x1 --> B65
    B7 -- x2 --> B65

    B69 -- x2 --> B70
    B27 -- x1 --> B70

    B9 -- x1 --> B73
    B15 -- x1 --> B73
    B7 -- x2 --> B73
    B3 -- x2 --> B73

    subgraph ThirdOrder
        B11[Mellow Milk Tea]
        B22[Pate de Campagne]
        B29[Honey-Pickled Nut & Berry Feast]
        B36[Colorful Hors D'oeuvre Selection]
        B47[Colorful Meat-Egg-Veggie Sandwich]
        B51[Melted Cheese Sun Bread]
        B57[Herbal Chicken Thigh Confit]
        B66[Rare Cheesecake]
        B71[Dried Fruit Granola]
        B75[Homemade Wine]
    end

    B10 -- x1 --> B11
    B4 -- x4 --> B11
    B79 -- x1 --> B11

    B21 -- x2 --> B22
    B39 -- x1 --> B22
    B41 -- x1 --> B22

    B28 -- x1 --> B29
    B69 -- x2 --> B29

    B35 -- x1 --> B36
    B31 -- x1 --> B36
    B41 -- x1 --> B36
    B45 -- x1 --> B36

    B46 -- x1 --> B47
    B21 -- x1 --> B47
    B35 -- x1 --> B47
    B49 -- x1 --> B47

    B50 -- x2 --> B51
    B41 -- x2 --> B51

    B31 -- x1 --> B57
    B79 -- x1 --> B57

    B65 -- x1 --> B66
    B41 -- x1 --> B66
    B27 -- x1 --> B66

    B70 -- x1 --> B71
    B16 -- x1 --> B71
    B27 -- x1 --> B71

    B73 -- x1 --> B75
    B27 -- x1 --> B75

    subgraph FourthOrder
        B12[High-Class Royal Milk Tea]
        B17[Claret Punch]
        B23[Wine-Cooked Melty Mutton]
        B55[Compote Maple Pancakes]
        B77[Homemade Brandy]
    end

    B11 -- x2 --> B12

    B16 -- x1 --> B17
    B75 -- x1 --> B17

    B22 -- x1 --> B23
    B75 -- x1 --> B23

    B51 -- x2 --> B55
    B16 -- x1 --> B55

    B75 -- x1 --> B77
    B1 -- x2 --> B77

    subgraph FifthOrder
        B13[Afternoon Tea Set]
        B18[Wine-Cooked Cinnamon Apples]
        B24[Roast Beef with Wasabi]
        B67[Brandy Apple Pie]
    end

    B12 -- x1 --> B13
    B54 -- x1 --> B13
    B66 -- x1 --> B13

    B17 -- x1 --> B18
    B75 -- x1 --> B18
    B15 -- x1 --> B18

    B23 -- x1 --> B24
    B36 -- x1 --> B24

    B66 -- x1 --> B67
    B77 -- x1 --> B67

    subgraph SixthOrder
        B14[Scarlet Afternoon Tea Set]
    end

    B13 -- x1 --> B14
    B21 -- x1 --> B14
    B31 -- x8 --> B14
    B33 -- x8 --> B14

    subgraph SeventhOrder
        B59[Orange Marmalade Jam]
    end

    B14 -- x1 --> B59
    B79 -- x1 --> B59

    subgraph EigthOrder
        B19[Crepes Suzette]
        B43[Fromage Blanc]
        B60[Vanilla Lemon Curd]
        B61[Fruit Basket]
    end

    B18 -- x1 --> B19
    B27 -- x1 --> B19
    B53 -- x2 --> B19
    B59 -- x1 --> B19

    B42 -- x1 --> B43
    B59 -- x1 --> B43

    B59 -- x1 --> B60
    B79 -- x1 --> B60
    B6 -- x1 --> B60
    B7 -- x2 --> B60

    B1 -- x2 --> B61
    B3 -- x2 --> B61
    B59 -- x1 --> B61
    B15 -- x2 --> B61

    subgraph NinthOrder
        B63[Chocolate & Banana Parfait]
    end

    B61 -- x1 --> B63
    B28 -- x1 --> B63

    subgraph FinalItems
        B20["Royal Fruit Ensemble"]
        B25["Soft Grilled Honey Mustard Chicken"]
        B30["Fruit-Nut-Cheese-Salami-Honey Bonanza"]
        B32["Super-Fresh Ham Saltimbocca"]
        B34["Huge Ratatouille Variety Quiche"]
        B38["Select Herbs & Melty Oxtail Soup"]
        B40["Fresh Variety Salad with Remoulade"]
        B44["Fromage Frais Gateau"]
        B48["Brioche French Toast"]
        B52["Eggs Benedict"]
        B56["Fluffy Lemon-Honey-Mint Souffle"]
        B58["Meat-Fish-Veggie Ajillo"]
        B62["Mango Bouquet"]
        B64["Queen Pineapple Parfait"]
        B68["Thick Cheese & Honey Apple Pie"]
        B72["Extra-Fruity Bircher Muesli"]
        B74["Fresh Veggie & Berry Yogurt Smoothie"]
        B76["Berry-Cinnamon Sangria"]
        B78["High-Grade Fruit Brandy"]
        B80["Mellow Aged Fermented Butter"]
    end

    B19 -- x1 --> B20
    B17 -- x1 --> B20

    B24 -- x1 --> B25
    B27 -- x2 --> B25

    B29 -- x1 --> B30
    B16 -- x1 --> B30
    B41 -- x2 --> B30

    B31 -- x1 --> B32
    B79 -- x1 --> B32

    B33 -- x2 --> B34
    B35 -- x1 --> B34

    B37 -- x2 --> B38
    B21 -- x1 --> B38
    B1 -- x2 --> B38

    B39 -- x2 --> B40
    B41 -- x1 --> B40
    B49 -- x1 --> B40

    B43 -- x1 --> B44
    B66 -- x1 --> B44
    B41 -- x2 --> B44

    B47 -- x1 --> B48
    B15 -- x2 --> B48
    B50 -- x1 --> B48
    B79 -- x1 --> B48

    B51 -- x1 --> B52
    B35 -- x1 --> B52
    B42 -- x1 --> B52
    B79 -- x1 --> B52

    B55 -- x1 --> B56
    B60 -- x1 --> B56
    B9 -- x1 --> B56

    B57 -- x1 --> B58
    B35 -- x1 --> B58
    B37 -- x1 --> B58

    B61 -- x2 --> B62
    B3 -- x2 --> B62

    B63 -- x1 --> B64
    B29 -- x1 --> B64

    B67 -- x1 --> B68
    B15 -- x2 --> B68
    B42 -- x1 --> B68
    B1 -- x2 --> B68

    B71 -- x1 --> B72
    B16 -- x1 --> B72
    B42 -- x1 --> B72

    B73 -- x1 --> B74
    B42 -- x1 --> B74
    B7 -- x3 --> B74
    B3 -- x3 --> B74

    B73 -- x2 --> B76
    B16 -- x1 --> B76
    B1 -- x3 --> B76
    B3 -- x1 --> B76

    B77 -- x2 --> B78
    B15 -- x1 --> B78
    B27 -- x1 --> B78

    B79 -- x3 --> B80
```
