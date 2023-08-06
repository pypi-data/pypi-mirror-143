function GetSizeFunction(kws, dataset, size_default) {
    if (kws.size_default || !kws.size_attribute) return size_default;

    let domain = d3.extent(dataset.nodes, d => d[kws.size_attribute]);
    if (kws.scale_domain_function) {
        domain = kws.scale_domain_function;
    }

    const SCALE = {
        "lineal": d3.scaleLinear,
        "pow": d3.scalePow,
        "sqrt": d3.scaleSqrt,
        "log": d3.scaleLog
    }

    let myScale = SCALE[kws.size_scale_type]()
        .domain(domain)
        .range(kws.scale_range_function)
        .clamp(true);

    const SizeFunction = (x) => {
        return myScale(x[kws.size_attribute])
    }
    return SizeFunction
}