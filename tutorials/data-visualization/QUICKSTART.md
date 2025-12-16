# Quick Start Guide - Data Visualization Tutorial

Get started with Python data visualization in 5 minutes!

## 🚀 Quick Install

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/strategickhaos-dao-llc/Sovereignty-Architecture-Elevator-Pitch-RedTeam.git
cd Sovereignty-Architecture-Elevator-Pitch-RedTeam

# Install visualization dependencies
pip install -r requirements.visualization.txt
```

## 📊 Run Your First Example

### Option A: Python Script (Fastest)

```bash
cd tutorials/data-visualization
python unemployment_plot.py
```

You should see a line chart showing US unemployment rates from 1980-2017!

### Option B: Jupyter Notebook (Interactive)

```bash
cd tutorials/data-visualization
jupyter notebook
```

Then:
1. Click on `unemployment_example.ipynb` in your browser
2. Click "Cell" → "Run All"
3. See your visualization!

## 📚 What's Included

| File | Description | Use When |
|------|-------------|----------|
| `1.3-python-data-visualization.md` | Tutorial text | You want to learn concepts |
| `unemployment_example.ipynb` | Interactive notebook | You want to experiment |
| `car_crashes_example.ipynb` | Interactive notebook | You want to explore more |
| `unemployment_plot.py` | Script | You want quick results |
| `car_crashes_plot.py` | Script | You want to see overlays |

## 🎯 Learning Path (15-30 minutes)

1. **Read** (5 min): Skim `1.3-python-data-visualization.md`
2. **Run** (5 min): Execute `unemployment_plot.py`
3. **Explore** (10 min): Open and run `unemployment_example.ipynb`
4. **Advanced** (10 min): Open and run `car_crashes_example.ipynb`
5. **Experiment**: Modify the code and see what happens!

## 💡 Pro Tips

### Modify the Examples

Try changing these values in the notebooks:

```python
# Change the plot color
color='steelblue'  → color='red'

# Change the figure size
figsize=(12, 6)  → figsize=(16, 8)

# Change the title
plt.title('U.S. Unemployment Rate (1980-2017)')  → plt.title('My Custom Title')
```

### Save Your Plots

Add this to any example:

```python
plt.savefig('my_plot.png', dpi=300, bbox_inches='tight')
```

### Use Your Own Data

Replace the sample data with your own:

```python
# Instead of:
years = list(range(1980, 2018))
unemployment_rate = [7.2, 7.6, ...]

# Use your data:
import pandas as pd
my_data = pd.read_csv('my_data.csv')
plt.plot(my_data['x_column'], my_data['y_column'])
```

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install -r requirements.visualization.txt
```

### "jupyter: command not found"
```bash
pip install jupyter notebook
```

### Plots don't show up
Make sure you have `plt.show()` at the end of your script.

### Want to use a virtual environment?
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.visualization.txt
```

## 🎓 Next Steps

After mastering these examples:

1. ✅ Read the full tutorial: `1.3-python-data-visualization.md`
2. ✅ Try the practice exercises in the tutorial
3. ✅ Experiment with [matplotlib gallery](https://matplotlib.org/stable/gallery/index.html)
4. ✅ Explore [seaborn examples](https://seaborn.pydata.org/examples/index.html)
5. ✅ Create visualizations with your own data!

## 📖 Additional Resources

- [Matplotlib Documentation](https://matplotlib.org)
- [Pandas Documentation](https://pandas.pydata.org)
- [NumPy Documentation](https://numpy.org)
- [Jupyter Tutorial](https://jupyter.org/try)

## ❓ Questions?

- Check the [tutorial README](README.md) for more details
- See the [implementation summary](SUMMARY.md) for technical info
- Open an issue in the repository for help

---

**Ready to visualize data like a pro? Start with `unemployment_plot.py` now!** 🚀
