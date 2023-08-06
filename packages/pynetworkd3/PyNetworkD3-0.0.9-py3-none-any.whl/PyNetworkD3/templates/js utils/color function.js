function GetColorFunction(kws, dataset, color_default) {
    if (kws.color_default || !kws.color_attribute) return color_default;

    const SCALE = {
        "lineal": d3.scaleSequential,
        "pow": d3.scaleSequentialPow,
        "sqrt": d3.scaleSequentialSqrt,
        "log": d3.scaleSequentialLog
    }

    if (kws.color_attribute_type == "categorical") {
        const color = d3.scaleOrdinal(d3["scheme" + kws.color_scheme]);
        if (kws.color_domain_function) {
            color.domain(kws.color_domain_function);
            if (kws.color_unknown) {
                color.unknown(kws.color_unknown)
            }
        }
        return (d) => color(d[kws.color_attribute]);
    }

    if (kws.color_attribute_type == "numerical") {
        let domain = d3.extent(dataset.nodes, d => d[kws.color_attribute]);
        if (kws.color_domain_function) {
            domain = kws.color_domain_function;
        }
        let interpolate = d3["interpolate" + kws.color_scheme]
        let color = SCALE[kws.color_scale_type](interpolate)
            .domain(domain)
            .clamp(true)

        if (kws.color_unknown) {
            let distance = Math.abs(domain[0] - domain[1]);

            function ColorWithUnknown(x) {
                let value = x[kws.color_attribute]
                let new_distance = Math.abs(domain[0] - value) + Math.abs(domain[1] - value);
                if (new_distance > distance) {
                    return kws.color_unknown
                }
                return color(value)
            }
            return ColorWithUnknown
        }
        return d => color(d[kws.color_attribute])
    }

    // ordinal
    let domain = [];
    if (kws.color_domain_function) {
        domain = kws.color_domain_function;
    } else {
        domain = new Set();
        dataset.nodes.forEach(d => {
            domain.add(d[kws.color_attribute])
        })
        domain = Array.from(domain);
        domain.sort(function(a, b) {
            if (a < b) { return -1; }
            if (a > b) { return 1; }
            return 0;
        });
    }
    let domainToId = {};
    domain.forEach((d, i) => domainToId[d] = i);
    let interpolate = d3["interpolate" + kws.color_scheme]
    let color = SCALE[kws.color_scale_type](interpolate)
        .domain([0, domain.length])
        .clamp(true)

    if (kws.color_domain_function) {
        function ColorWithUnknown(x) {
            let value = x[kws.color_attribute]
            if (domainToId[value] !== undefined) return color(domainToId[value]);
            return kws.color_unknown ? kws.color_unknown : "black";
        }
        return ColorWithUnknown
    }
    return d => color(domainToId[d[kws.color_attribute]])
}