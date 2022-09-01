import os
import json
import shutil
import subprocess


TEMP_DIR = os.path.abspath("blobs")

INPUT_FILES = [
#     "../../../../5_dataset/test_instances.jsonl",
#     "../../../compare_recipes/docker-gen-tool/results_docker-english_test_recipes.jsonl",
#     "../../../compare_recipes/docker-gen-tool/results_docker-english_test_recipes.jsonl",
#     "../../../compare_recipes/docker-gen-tool/results_docker-english_test_recipes.jsonl"
    "../../new_recipes/results_docker-eng@0.7-1840000_test_recipes.jsonl",
    "../../new_recipes/results_docker-eng@0.8-1840000_test_recipes.jsonl",
    "../../new_recipes/results_docker-eng@0.9-1840000_test_recipes.jsonl",
    "../../new_recipes/results_docker-eng@1-1840000_test_recipes.jsonl"
    ]

RECIPES_DIR = os.path.abspath("recipes")


def execute_cmd(command):
    with subprocess.Popen(args=command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as p:
        stdout = list()
        for line in p.stdout:
            line = line.decode("utf-8")
            stdout.append(line)
            print(line)  # process line here
        status = p.wait()

    return status, stdout


def cleanup():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)


if __name__ == "__main__":
    # INPUT_FILES = [os.path.join(RECIPES_DIR, f) for f in os.listdir(RECIPES_DIR)]

    for input_file in INPUT_FILES:
        input_file = os.path.abspath(input_file)
        if not input_file.endswith(".jsonl"):
            continue
        print("processing", input_file)

        cleanup()

        with open(input_file) as f:
            for i, line in enumerate(f.readlines()):
                print(i+1)
                recipe = json.loads(line.strip())

                sha = recipe["sha1"] if "sha1" in recipe.keys() else recipe["source_sha1"]
                dockerfile_name = os.path.join(TEMP_DIR,  sha + ".Dockerfile")
                with open(dockerfile_name, "w") as f:
                    f.write(recipe["blob_nocomments"])

            status, stdout = execute_cmd("bash clean_outputs.sh")
            if status != 0:
                print("Error status:", status)
                exit(1)

            status, stdout = execute_cmd("bash run_pipeline.sh")
            # with open("output.txt", "w") as f:
            #     f.writelines(stdout)
            if status != 0:
                print("Error status:", status)
                exit(1)

            shutil.copyfile(os.path.join("2-phase-2-dockerfile-asts", "outputs", "blobs_asts_p2.jsonl"), os.path.basename(input_file).replace(".jsonl", "_blobs_asts_p2.jsonl"))

    cleanup()

    print("+++ Operation completed +++")