---
layout: post
title: "Mortgage calculator"
author: "Mario"
date: 2026-07-04
usemathjax: true
---

# Mortgage calculator

I don't like the mortgage calculators banks put on their website.
You type in a bunch of numbers and then you get one number back.

Life moves much faster than this.
Now you think it's 30 years, then it's 25, mmmh, and how about an interest rate of 5.5% p.a. instead of 4.8% p.a.
You don't want to type that in each time, do you?

These mortgage calculators are also not showing all the information.
Rarely do you see straight away how much interest you have to pay.
For a 30-year loan that can be as much as the principal loan you want to borrow.

Worst of all, you wouldn't learn how beautiful [amortization](https://en.wikipedia.org/wiki/Amortization_(accounting)){:target="_blank"} can look like.
And that would be a shame.

  <script src="https://d3js.org/d3.v7.min.js"></script>

  <style>

    .note {
      max-width: 1050px;
      font-size: 14px;
      color: #555;
      line-height: 1.45;
      margin-bottom: 18px;
    }

    .controls {
      display: grid;
      grid-template-columns: 180px 1fr 130px;
      gap: 8px 12px;
      max-width: 1050px;
      align-items: center;
      margin-bottom: 18px;
      padding: 14px;
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
    }

    label {
      font-size: 14px;
      font-weight: 600;
    }

    input[type="range"] {
      width: 100%;
    }

    .value {
      font-variant-numeric: tabular-nums;
      font-size: 14px;
      text-align: right;
    }

    .result {
      max-width: 1050px;
      margin: 0 0 16px 0;
      padding: 12px 14px;
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 15px;
    }

    svg {
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      max-width: 100%;
      height: auto;
    }

    .axis-title {
      font-size: 14px;
      font-weight: 700;
      fill: #222;
    }

    .small {
      font-size: 11px;
      fill: #666;
    }

    .contour {
      fill: none;
      stroke: #333;
      stroke-width: 1.2;
      stroke-opacity: 0.65;
    }

    .contour.major {
      stroke-width: 1.8;
      stroke-opacity: 0.9;
    }

    .contour-label {
      font-size: 11px;
      font-weight: 700;
      fill: #222;
      paint-order: stroke;
      stroke: white;
      stroke-width: 4px;
      stroke-linejoin: round;
    }

    .guide-line {
      stroke: #1f77b4;
      stroke-width: 1.4;
      stroke-dasharray: 4 4;
    }

    .selected-point {
      fill: #1f77b4;
      stroke: white;
      stroke-width: 2.5;
      cursor: grab;
    }

    .readout-label {
      font-size: 13px;
      font-weight: 700;
      fill: #1f77b4;
      paint-order: stroke;
      stroke: white;
      stroke-width: 4px;
      stroke-linejoin: round;
    }

    .drag-capture {
      fill: transparent;
      cursor: crosshair;
    }

    .repayment-line {
      fill: none;
      stroke: #1f77b4;
      stroke-width: 3;
      stroke-opacity: 0.85;
    }

    .axis path,
    .axis line {
      stroke: #333;
    }

    .axis text {
      font-size: 11px;
    }
  </style>

The contour lines show combinations of **interest rate** and **loan term** that produce the same monthly repayment for the selected loan amount. This makes the trade-off visible: for a fixed loan, a shorter term can have the same repayment effect as a higher interest rate, and vice versa. 

<div class="controls">
  <label for="principal">Loan amount</label>
  <input id="principal" type="range" min="50000" max="1500000" step="10000" value="650000">
  <div id="principalValue" class="value"></div>

  <label for="rate">Annual interest rate</label>
  <input id="rate" type="range" min="0.5" max="12" step="0.1" value="6.5">
  <div id="rateValue" class="value"></div>

  <label for="term">Loan term</label>
  <input id="term" type="range" min="5" max="35" step="1" value="25">
  <div id="termValue" class="value"></div>
</div>

<div class="result" id="result"></div>

<svg id="viz" width="1100" height="760" viewBox="0 0 1100 760"></svg>

<script>
  // ------------------------------------------------------------
  // Amortisation formula
  // ------------------------------------------------------------
  function monthlyPayment(principal, annualRatePct, years) {
    const monthlyRate = annualRatePct / 100 / 12;
    const n = years * 12;

    if (monthlyRate === 0) {
      return principal / n;
    }

    return principal * monthlyRate * Math.pow(1 + monthlyRate, n) /
      (Math.pow(1 + monthlyRate, n) - 1);
  }

  function fmtMoney(x) {
    return "$" + d3.format(",.0f")(x);
  }

  function fmtMoney2(x) {
    return "$" + d3.format(",.2f")(x);
  }

  function clamp(x, lo, hi) {
    if (!Number.isFinite(x)) return lo;
    return Math.max(lo, Math.min(hi, x));
  }

  // ------------------------------------------------------------
  // SVG setup
  // ------------------------------------------------------------
  const svg = d3.select("#viz");

  const W = 1100;
  const H = 760;

  const plot = {
    x0: 115,
    y0: 75,
    width: 850,
    height: 570
  };

  plot.x1 = plot.x0 + plot.width;
  plot.y1 = plot.y0 + plot.height;

  const rateDomain = [0.5, 12];
  const termDomain = [5, 35];

  // Term is horizontal, interest is vertical.
  // Both are linearly spaced.
  const xTerm = d3.scaleLinear()
    .domain(termDomain)
    .range([plot.x0, plot.x1]);

  const yRate = d3.scaleLinear()
    .domain(rateDomain)
    .range([plot.y1, plot.y0]);

  const principalInput = d3.select("#principal");
  const rateInput = d3.select("#rate");
  const termInput = d3.select("#term");

  const principalValue = d3.select("#principalValue");
  const rateValue = d3.select("#rateValue");
  const termValue = d3.select("#termValue");
  const result = d3.select("#result");

  // ------------------------------------------------------------
  // Static axes
  // ------------------------------------------------------------
  svg.append("text")
    .attr("class", "axis-title")
    .attr("x", (plot.x0 + plot.x1) / 2)
    .attr("y", 35)
    .attr("text-anchor", "middle")
    .text("Equal monthly repayment contours");

  svg.append("text")
    .attr("class", "small")
    .attr("x", (plot.x0 + plot.x1) / 2)
    .attr("y", 55)
    .attr("text-anchor", "middle")
    .text("Click or drag in the plot, or use the sliders");

  const xAxis = d3.axisBottom(xTerm)
    .tickValues(d3.range(5, 36, 5))
    .tickFormat(d => d + " years");

  const yAxis = d3.axisLeft(yRate)
    .tickValues([0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    .tickFormat(d => d + "%");

  svg.append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${plot.y1})`)
    .call(xAxis);

  svg.append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${plot.x0},0)`)
    .call(yAxis);

  svg.append("text")
    .attr("class", "axis-title")
    .attr("x", (plot.x0 + plot.x1) / 2)
    .attr("y", plot.y1 + 55)
    .attr("text-anchor", "middle")
    .text("Loan term");

  svg.append("text")
    .attr("class", "axis-title")
    .attr("x", -((plot.y0 + plot.y1) / 2))
    .attr("y", 38)
    .attr("transform", "rotate(-90)")
    .attr("text-anchor", "middle")
    .text("Annual interest rate");

  // Light grid
  svg.append("g")
    .attr("opacity", 0.15)
    .selectAll("line.vertical-grid")
    .data(d3.range(5, 36, 5))
    .enter()
    .append("line")
    .attr("x1", d => xTerm(d))
    .attr("x2", d => xTerm(d))
    .attr("y1", plot.y0)
    .attr("y2", plot.y1)
    .attr("stroke", "#000");

  svg.append("g")
    .attr("opacity", 0.15)
    .selectAll("line.horizontal-grid")
    .data(d3.range(1, 13, 1))
    .enter()
    .append("line")
    .attr("x1", plot.x0)
    .attr("x2", plot.x1)
    .attr("y1", d => yRate(d))
    .attr("y2", d => yRate(d))
    .attr("stroke", "#000");

  // ------------------------------------------------------------
  // Dynamic layers
  // ------------------------------------------------------------
  const contourLayer = svg.append("g");
  const labelLayer = svg.append("g");

  const selectedContourLayer = svg.append("g");

  const termGuide = svg.append("line")
    .attr("class", "guide-line");

  const rateGuide = svg.append("line")
    .attr("class", "guide-line");

  const selectedPoint = svg.append("circle")
    .attr("class", "selected-point")
    .attr("r", 8);

  const selectedLabel = svg.append("text")
    .attr("class", "readout-label");

  const dragCapture = svg.append("rect")
    .attr("class", "drag-capture")
    .attr("x", plot.x0)
    .attr("y", plot.y0)
    .attr("width", plot.width)
    .attr("height", plot.height);

  // ------------------------------------------------------------
  // Contour generation
  // ------------------------------------------------------------
  const nx = 180;
  const ny = 180;

  const termValues = d3.range(nx).map(i =>
    termDomain[0] + i * (termDomain[1] - termDomain[0]) / (nx - 1)
  );

  const rateValues = d3.range(ny).map(j =>
    rateDomain[1] - j * (rateDomain[1] - rateDomain[0]) / (ny - 1)
  );

  const contourGenerator = d3.contours()
    .size([nx, ny])
    .smooth(true);

  function niceContourLevels(principal) {
    const minPay = monthlyPayment(principal, rateDomain[0], termDomain[1]);
    const maxPay = monthlyPayment(principal, rateDomain[1], termDomain[0]);

    const step = chooseStep(maxPay - minPay);

    const start = Math.ceil(minPay / step) * step;
    const end = Math.floor(maxPay / step) * step;

    return d3.range(start, end + step * 0.5, step);
  }

  function chooseStep(range) {
    if (range <= 1500) return 100;
    if (range <= 3000) return 250;
    if (range <= 8000) return 500;
    if (range <= 15000) return 1000;
    return 2000;
  }

  function gridValues(principal) {
    const values = [];

    for (let j = 0; j < ny; j++) {
      for (let i = 0; i < nx; i++) {
        values.push(
          monthlyPayment(principal, rateValues[j], termValues[i])
        );
      }
    }

    return values;
  }

  function contourPath(d) {
    const path = d3.geoPath(
      d3.geoTransform({
        point: function(px, py) {
          const term = termDomain[0] + px * (termDomain[1] - termDomain[0]) / (nx - 1);
          const rate = rateDomain[1] - py * (rateDomain[1] - rateDomain[0]) / (ny - 1);
          this.stream.point(xTerm(term), yRate(rate));
        }
      })
    );

    return path(d);
  }

  function drawContours(principal) {
    const values = gridValues(principal);
    const levels = niceContourLevels(principal);

    const contours = contourGenerator
      .thresholds(levels)(values);

    contourLayer.selectAll("*").remove();
    labelLayer.selectAll("*").remove();

    contourLayer.selectAll("path")
      .data(contours)
      .enter()
      .append("path")
      .attr("class", d => d.value % (levels[1] - levels[0] === 0 ? 1 : 2 * (levels[1] - levels[0])) === 0
        ? "contour major"
        : "contour"
      )
      .attr("d", contourPath);

    // Place labels near the right side by solving for rate at a chosen term.
    // This avoids clutter and keeps labels readable.
    contours.forEach((c, idx) => {
      const repayment = c.value;

      // Try a few label positions; keep the first valid one.
      const candidateTerms = [31, 27, 23, 19, 15, 11];

      let label = null;

      for (const term of candidateTerms) {
        const rate = solveRateForPayment(principal, term, repayment);

        if (rate !== null && rate >= rateDomain[0] && rate <= rateDomain[1]) {
          const x = xTerm(term);
          const y = yRate(rate);

          // Estimate local angle using neighboring term.
          const rate2 = solveRateForPayment(principal, term + 0.4, repayment);
          let angle = 0;

          if (rate2 !== null) {
            const x2 = xTerm(term + 0.4);
            const y2 = yRate(rate2);
            angle = Math.atan2(y2 - y, x2 - x) * 180 / Math.PI;
          }

          label = { x, y, angle };
          break;
        }
      }

      if (label) {
        labelLayer.append("text")
          .attr("class", "contour-label")
          .attr("x", label.x)
          .attr("y", label.y - 4)
          .attr("text-anchor", "middle")
          .attr("transform", `rotate(${label.angle},${label.x},${label.y})`)
          .text(fmtMoney(repayment));
      }
    });
  }

  function solveRateForPayment(principal, term, targetPayment) {
    let lo = rateDomain[0];
    let hi = rateDomain[1];

    const fLo = monthlyPayment(principal, lo, term);
    const fHi = monthlyPayment(principal, hi, term);

    if (targetPayment < fLo || targetPayment > fHi) {
      return null;
    }

    for (let k = 0; k < 40; k++) {
      const mid = (lo + hi) / 2;
      const fMid = monthlyPayment(principal, mid, term);

      if (fMid < targetPayment) {
        lo = mid;
      } else {
        hi = mid;
      }
    }

    return (lo + hi) / 2;
  }

  // ------------------------------------------------------------
  // Selected contour
  // ------------------------------------------------------------
  function drawSelectedContour(principal, selectedPayment) {
    selectedContourLayer.selectAll("*").remove();

    const values = gridValues(principal);
    const c = contourGenerator
      .thresholds([selectedPayment])(values)[0];

    if (!c) return;

    selectedContourLayer.append("path")
      .datum(c)
      .attr("class", "repayment-line")
      .attr("d", contourPath);
  }

  // ------------------------------------------------------------
  // Interaction
  // ------------------------------------------------------------
  function setRateTermFromPointer(event) {
    // d3.drag passes a custom drag event.
    // For click events, use the event directly.
    // For drag events, use event.sourceEvent, which is the original mouse/pointer event.
    const source = event.sourceEvent || event;

    // Always compute coordinates relative to the SVG, not relative to the event target.
    const [mx, my] = d3.pointer(source, svg.node());

    const termRaw = xTerm.invert(mx);
    const rateRaw = yRate.invert(my);

    const term = Math.round(clamp(termRaw, termDomain[0], termDomain[1]));
    const rate = Math.round(clamp(rateRaw, rateDomain[0], rateDomain[1]) * 10) / 10;

    termInput.property("value", term);
    rateInput.property("value", rate);

    update(false);
  }

  dragCapture
    .on("click", setRateTermFromPointer)
    .call(
      d3.drag()
        .on("start", setRateTermFromPointer)
        .on("drag", setRateTermFromPointer)
    );

  principalInput.on("input", () => update(true));
  rateInput.on("input", () => update(false));
  termInput.on("input", () => update(false));

  function update(redrawContours) {
    const principal = +principalInput.property("value");
    const rate = +rateInput.property("value");
    const term = +termInput.property("value");

    const payment = monthlyPayment(principal, rate, term);
    const totalPaid = payment * term * 12;
    const totalInterest = totalPaid - principal;

    principalValue.text(fmtMoney(principal));
    rateValue.text(d3.format(".1f")(rate) + "% p.a.");
    termValue.text(term + " years");

    result.html(`
      <strong>Monthly repayment:</strong> ${fmtMoney2(payment)}
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>Total paid:</strong> ${fmtMoney2(totalPaid)}
      &nbsp;&nbsp;|&nbsp;&nbsp;
      <strong>Total interest:</strong> ${fmtMoney2(totalInterest)}
    `);

    if (redrawContours) {
      drawContours(principal);
    }

    drawSelectedContour(principal, payment);

    const x = xTerm(term);
    const y = yRate(rate);

    rateGuide
      .attr("x1", plot.x0)
      .attr("x2", x)
      .attr("y1", y)
      .attr("y2", y);

    termGuide
      .attr("x1", x)
      .attr("x2", x)
      .attr("y1", y)
      .attr("y2", plot.y1);

    selectedPoint
      .attr("cx", x)
      .attr("cy", y);

    selectedLabel
      .attr("x", x + 14)
      .attr("y", y - 14)
      .text(`${d3.format(".1f")(rate)}%, ${term}y → ${fmtMoney2(payment)}`);
  }

  // Initial draw
  drawContours(+principalInput.property("value"));
  update(false);
</script>


# Technical details

The equation for a fixed scheduled repayment \\(M\\) of a principal loan \\(P\\) over a number of periods \\(n\\) with an interest rate \\(r\\) is

$$
M = P \frac{r(1+r)^n}{(1+r)^n-1}.
$$

In case of monthly repayments, we divide the annual interest rate (it's usually given as % p.a., which is short for *per annum*, which is Latin for per year) by 12 and have to multiply \\(n\\) with 12 if the duration of the term is in years.

Let's find out under what conditions the principal equals the interest paid.

The total amount repaid is \\(n\,M\\).
The total interest is \\(I = n\,M - P\\).
And we want:

$$
I = P
$$

A little algebra turns this into

$$
n\,M - P = P
$$

or:

$$
n\,M = 2P
$$

We can substitute the amortization formula back for \\(M\\):

$$
n\,P \frac{r(1+r)^n}{(1+r)^n-1} =  2P
$$

\\(P\\) cancels out.
This means our answer doesn't depend on the principal loan amount \\(P\\).

We are left with

$$
n\frac{r(1+r)^n}{(1+r)^n-1} = 2
$$

We can rewrite \\(r\\) and \\(n\\) in annual-rates-and-years form.
With \\(R\\) as the annual interest rate and \\(T\\) as term in years we have \\(r = \frac{R}{12}\\) and \\(n=12\,T\\).
So

$$
n\,r = 12\,T \cdot \frac{R}{12} = R\,T
$$

The exact condition becomes

$$
\frac{R\,T(1+\frac{R}{12})^{12\,T}}{(1+\frac{R}{12})^{12\,T}-1} = 2
$$

The quality of principal and interest depends mostly on the product \\(R\,T\\), or the annual rate \\(\times\\) years.

We can get a useful heuristic when we replace monthly compounding with annual compounding

$$
\left(1+\frac{R}{12}\right)^{-12\,T} \approx e^{-R\,T}
$$

Then the condition becomes

$$
\frac{R\,T}{1-e^{-R\,T}} = 2
$$

Let \\(x = R\,T\\), then

$$
\frac{x}{1-e^{-x}} = 2
$$

This equation has the solution \\(x \approx 1.594\\).
So the mental rule is \\(\boxed{\text{annual rate}\;\times\;\text{years} \approx 1.6}\\).

Examples:

$$
0.053\,\times\,30 \approx 1.59
$$

So whenever you find a loan in the wild where the product of annual interest rate times its duration equals 1.6 you know that someone is paying the same amount on interest as their loan is worth.
