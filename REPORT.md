## SMAP Full Stacks Coding Challenge

#### Brief Introduction:
Frontend is used to visualize the data. There's two html pages to display information:
- summary.html
- detail.html

Summary.html is used to display the breakdown of total consumption by all users / months - This is shown in a bar chart.
In addition, I have used further aggregation of data by showing a line graph for the average consumption / months.

Detail.html shows further breakdown of information for an induvidual user such as total consumpion, average consumption, area & tariff. 

Backend uses two views for the rendering of the pages listed above. 
I have also used two models (user_data and consumption_data) which is a many-to-one relationship between them.

Tests were carried out by using Django's build-in testing, I used this to test out models and aggregation of consumption data. I also tested the import command and views.

### Installation Guide:

```
1) Fork or download repository
2) Install virtualenv
3) Install Django version 1.11
4) Create migration for the models - python manage.py makemigration consumption
5) Migrate! python manage.py migrate
6) Import user and consumption data - python manage.py import
```

### Tools Used:

- Library for Data Visualization: ChartJS
- Browser: Google Chrome
- Text editor: Visual Studio Code

### Final Conclusion:

> Please hire me! :smile:
