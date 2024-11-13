---
layout: post
title: "The data generating process"
author: "Mario"
date: 2024-11-06
---

Hello. If you, like me, are looking at data all day every day (or just sometimes), you want to start thinking about *The Data Generating Process*. According to one of the shortest articles I've seen on [Wikipedia](https://en.wikipedia.org/wiki/Data_generating_process)
> a **data generating process** is a process in the real world that "generates" the data one is interested in.

Thinking about the data generating process has been a game changer for me.

Before getting into the weeds, let's unpack what *data generating process* means and how you can can use it as a mental model. If we flip *data generating process* around, we get the sentence:

**Processes generate data.**

1. [**Process**](https://www.websters1913.com/words/Process) is "a series of actions, motions, or occurrences".
2. [**Generate**](https://www.websters1913.com/words/Generate) means "to bring to life".
3. [**Data**](https://www.websters1913.com/words/Datum) (plural for datum) are "facts or principles granted"

I like those old dictionary definitions. [Webster's 1913](http://jsomers.net/blog/dictionary) is particularly rewarding in its essence and clarity. Using our new words (or old?), let's create a more vivid description of *data generating process*:

**A series of actions, motions, or occurrences bring to life facts.**

Splendid!

Isn't that how we think the world keeps going? I think so, too: Something is going on, and "poof!", there's an outcome, and when we look at it we try to make sense about what was causing the outcome. What is that Something? And that Something is the (*data generating*) *process*.

Let's say you are looking at a series of data points, for example, a time series. Depending on the domain, you might describe what you see as follows:

- "The numbers go up and down a lot, but over time you can see which way things are moving." (Election Polls)
- "There's a general upward trend, but with occasional periods of decline." (Stock Market)
- "Over time, things are getting warmer, though there are still some cooler periods." (Climate Change)
- "The trend is upward, but sales can vary a lot from month to month." (Retail Sales)

# Fact number one: Looking at data makes you think about the *What*.

That's good but not good enough. You can do better. You want to understand "Why" things are the way they are and "How" they came to be.[^1] You are describing that facts but you are not (yet) looking into what kinds of actions have brought those facts to life. If you were to think about *actions, motions, or occurrences*, you start thinking about what those actions, motions, or occurences would give rise to.

I look at data a lot. Being a climate data scientist, I am curious about the past, the present, and the future of the climate system. Climate science, as a discipline, is rich in data. There are about 17,500 stations around the world that record weather data ([source](https://wmo.int/activities/global-observing-system-gos/global-observing-system-gos)). There are currently 322 earth observation satellites in orbit around Earth ([source](https://wmo.int/topics/earth-observation-satellites)). We do that because

> Accurate weather forecast and climate prediction are crucial for decision making and support for appropriate action to mitigate the impacts of natural hazards and climate change. \- [WMO](https://wmo.int)

Weather forecast goes beyond looking at data. And that brings us to fact number two.

# Fact number two: Generating data makes you think about the *How*.

Here, by data I mean fake data[^2]. Yes, I am saying that you should create fake data. Everyone should. You might actually learn something. Creating fake data is not easy. Particularly, if you want to make your fake data look real. Here's a challenge.

Try to fake the [US stock market data](https://tradingeconomics.com/united-states/stock-market) for the last 50 years!

![](/assets/spx_ind.png)

Or, take [Global Temperature](https://climate.nasa.gov/vital-signs/global-temperature/?intent=111). Try faking that.

![](/assets/GlobalTemp.png)

## A brief history of weather forecasting

Let's look at weather forecast again because it's a prime example of how we got from looking at data to making predictions (about the weather). According to [history](https://teachersinstitute.yale.edu/curriculum/units/1994/5/94.05.01/2), the Greeks where one of the first meteorologists, and Aristotle is considered the founder of meteorology, having written his [“Meteorological”](https://en.wikipedia.org/wiki/Meteorology_(Aristotle)) around 340 B.C. Skipping ahed 2200 years and we are witnessing  [the birth of modern weather forecasting](https://www.bbc.com/news/magazine-32483678) in the 1860s.

Today, numeral weather prediction models are tools of the trade for meteorologists and climate scientists. [Weather forecasts have become much more accurate](https://ourworldindata.org/weather-forecasts): "A four-day forecast today is as accurate as a one-day forecast 30 years ago." We all use weather forecast data on a daily basis on our phones. Open your weather app and you are likely to find some information about the data. If I scroll down on my iPhone weather app, for example, I can find a link to [weather data](https://support.apple.com/en-nz/105038). At the bottom of the page, you will find all the data sources the iPhone weather uses. (All of this is fake data, but in the best and most useful way imaginable.)

By the way, predicting the weather is way easier than predicting the stock market. But that's another topic.

Now, how can you actually generate data? In practice, you can run numerical simulations of the thing you are interested in. That is usually some sort of computer program that will generate some data outputs for you.

Weather forecasting itself is too complicated for this post, so I'll guide you through a simpler, yet, as insightful, example.

## The *coin toss*

One of my favourite examples for everything is the coin toss. Everyone has a coin and can flip it. It's a real-world process and one that is simple enough to help our understanding.

Depending how many times you flip the coin you generate observations, or data, from that process. You guessed it, the coin toss itself is a *data generating process*.

Here's a coin toss example in Python. (You can copy it or download it [here](/assets/coin_toss.py).)

```python
import random

def coin_toss(num_tosses,p_head):
    return random.choices(["H", "T"], weights=[p_head, 1-p_head], k=num_tosses)

if __name__ == "__main__":
    num_tosses = int(input("Number of coin tosses: "))
    p_head = float(input("Probability of tossing heads (between 0 and 1, default=0.5): ") or "0.5")
    tosses = coin_toss(num_tosses, p_head)
    print(f"Results after {num_tosses} tosses:")
    print(", ".join(tosses))
    heads_count = tosses.count("H")
    print(f"Heads: {heads_count}")
    tails_count = tosses.count("T")
    print(f"Tails: {tails_count}")
```

The method `coin_toss()` generates our facts which we record in the variable `tosses`. My output from tossing 10 times using the default probability of 0.5 is

```
Number of coin tosses: 10
Probability of tossing heads (between 0 and 1, default=0.5): 
Results after 10 tosses:
H, H, T, T, H, T, T, T, H, T
Heads: 4
Tails: 6
```

Now that we have a model of our coin toss world, we can create different outcomes every time we run the code example. We can pick probabilities that are different from a fair coin (p=0.5). We can repeat the coin toss but for more tosses. Here's a thousand, with a probability of heads of 0.2.

```
Number of coin tosses: 1000
Probability of tossing heads (between 0 and 1, default=0.5): 0.2
Results after 1000 tosses:
H, H, T, T, T, T, T, T, H, T, H, T, T, H, T, T, H, T, T, T, T, T, T, H, T, T, H, T, T, H, H, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, H, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, H, T, T, T, T, T, T, T, T, T, H, T, T, H, H, T, T, T, T, T, T, H, T, H, T, H, H, T, H, T, T, T, T, T, T, T, T, T, H, T, T, T, H, T, T, H, T, T, T, T, H, H, T, T, T, T, T, T, T, T, H, T, H, T, T, T, T, T, H, T, T, H, T, H, T, H, T, T, T, T, T, H, T, T, H, T, H, T, T, T, T, H, T, T, H, T, T, T, T, T, H, T, T, T, T, H, T, T, T, T, T, T, H, T, T, T, T, H, T, T, T, T, H, T, T, H, T, T, T, T, T, H, H, T, T, H, T, T, T, T, H, T, T, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, H, H, T, H, H, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, H, H, T, T, H, T, T, T, T, T, T, T, H, T, T, T, T, H, T, T, T, T, H, T, T, T, T, T, H, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, H, T, T, T, T, T, T, H, T, T, H, T, T, T, T, T, T, T, T, H, T, H, T, T, T, T, H, T, T, T, T, T, T, T, T, H, T, T, T, T, T, H, H, T, T, H, T, H, T, H, T, T, T, T, H, H, H, T, T, T, H, T, T, T, H, T, T, T, T, T, T, H, T, T, H, T, T, H, T, T, T, T, T, H, T, H, T, T, H, T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, H, T, H, H, T, T, T, T, T, H, T, H, H, T, H, T, T, T, T, T, T, T, T, H, T, T, T, H, H, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, H, H, T, T, T, H, H, T, T, T, T, T, T, H, H, T, H, H, T, H, T, H, T, H, T, H, T, H, T, T, T, H, T, T, T, T, T, H, T, H, T, T, T, T, T, H, H, H, T, T, H, T, T, T, H, T, T, T, T, T, T, T, T, T, H, H, H, H, H, H, H, T, T, T, T, H, T, T, H, T, T, T, T, T, H, T, T, T, H, T, H, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, T, T, T, H, H, T, T, H, T, T, T, T, T, H, T, T, T, T, T, T, T, H, T, T, H, T, T, T, H, H, T, T, T, T, T, T, T, T, T, H, T, T, H, T, T, T, H, T, T, H, T, T, T, T, T, T, T, T, H, T, T, H, T, H, T, H, T, H, T, T, T, H, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, H, T, T, T, T, T, T, H, T, H, T, H, T, T, H, H, T, T, T, T, H, T, T, T, T, T, T, T, T, H, T, H, H, H, T, T, T, T, H, T, T, H, T, T, H, T, T, H, T, T, T, T, H, T, T, H, T, T, H, T, T, H, T, H, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, T, T, T, H, T, H, T, T, T, H, T, H, H, T, T, T, T, T, H, T, T, T, T, T, T, T, H, H, T, T, T, T, T, H, T, T, T, T, T, T, H, T, T, T, T, T, T, T, T, T, T, H, H, T, T, T, T, T, H, T, T, T, H, H, T, H, T, T, T, H, T, T, T, T, H, T, H, T, T, T, T, T, T, T, T, T, H, T, H, T, T, T, T, T, T, T, T, T, T, T, T, H, H, T, T, T, T, T, T, T, T, T, T, T, H, T, T, T, T, H, T, T, T, T, H, T, T, T, T, H, H, T, T, T, T, T, T, T
Heads: 218
Tails: 782
```

We can see that we don't always get the exact share of heads and tails (200 H out of 1000 tosses) and that's ok. Tossing a coin, as we know from the real world creates different outcomes every time we do it. That's why in football

> the referee tosses a coin and the team that wins the toss decides which goal to attack in the first half or to take the kick-off. \- [Law 8: The Start and Restart of Play](https://www.thefa.com/football-rules-governance/lawsandrules/laws/football-11-11/law-8---the-start-and-restart-of-play) 

That's why our model contains randomness in the first place (`random.choices(["H", "T"],...)`. We know that coin tossing looks random, so our model must reflect the fact.

# Fact number three: Examining your model lets you figure out the *Why*.

That's it. The *data generating process*.

[^1]: In his book [Start with WHY](https://simonsinek.com/books/start-with-why/), Simon Sinek lines up the "What", the "How", and the "Why" in what he calls *The Golden Circle*.
[^2]: To sound more professional, you should call it *synthetic data*.
