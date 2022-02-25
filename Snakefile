
rule generate_numbers:
    input:
        csv="iris.csv"
    conda:
        "environment.yaml"
    output:
        data="generator/data.npz",
        label="generator/targets.json"
    log:
        "logs/generate-numbers.log"
    shell:
        "python generate-numbers.py --csvpath {input.csv} --outpath {output.data} --targetjson {output.label} --logpath {log}"
        
        
rule process_numbers:
    input:
        data="generator/data.npz",
        label="generator/targets.json"
    conda:
        "environment.yaml"
    output:
        "data/2d.csv"
    log:
        "logs/process-numbers.log"
    shell:
        "python process-numbers.py --datapath {input.data} --targetpath {input.label} --outpath {output} --logpath {log}"
        
        
rule plot_to_file:
    input:
        csv="data/2d.csv"
    conda:
        "environment.yaml"
    output:
        "plot/scatter.png"
    log:
        "logs/plot-to-file.log"
    shell:
        "python plot-to-files.py --datapath {input.csv} --outpath {output} --logpath {log}"

