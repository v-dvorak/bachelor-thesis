import argparse
import json
from pathlib import Path

from . import Utils
from .Conversions import Formatter
from .Conversions.Formats import InputFormat, OutputFormat
from .Stats import Plots
from .Stats.StatJob import StatJob
from .Val import EvalJob


def main():
    parser = argparse.ArgumentParser(
        prog="Object Detection Tools"
    )
    subparsers = parser.add_subparsers(dest="command", help="Jobs")

    # region DATASET FORMATTING AND SPLITTING ARGUMENTS
    form_parser = subparsers.add_parser("form")
    form_parser.add_argument("output", help="Transformed dataset destination.")
    form_parser.add_argument("image_dir", help="Path to images.")
    form_parser.add_argument("annot_dir", help="Path to annotations.")

    form_parser.add_argument("-i", "--input_format", default=InputFormat.MUNG.value,
                             choices=InputFormat.get_all_value())
    form_parser.add_argument("-o", "--output_format", default=OutputFormat.COCO.value,
                             choices=OutputFormat.get_all_value())
    form_parser.add_argument("--image_format", default="jpg", help="Input image format.")

    form_parser.add_argument("-s", "--split", type=float, default=1.0, help="Train/test split ratio.")

    form_parser.add_argument("--seed", type=int, default=42, help="Seed for dataset shuffling.")
    form_parser.add_argument("--resize", type=int, default=None,
                             help="Resizes images so that the longer side is this many pixels long.")
    form_parser.add_argument("--image_splitting", action="store_true", help="Split images into smaller ones.")
    form_parser.add_argument("-a", "--augmentation", nargs="+", default=None, help="Zoom in/out augmentations.")

    # global arguments
    form_parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
    form_parser.add_argument("--config", default=None,
                             help="Path to config, see \"default.config\" for example.")
    # endregion

    # region DATASET SPLITTING ARGUMENTS
    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("output", help="Split dataset destination.")
    split_parser.add_argument("image_dir", help="Path to images.")
    split_parser.add_argument("annot_dir", help="Path to annotations.")

    split_parser.add_argument("-s", "--split", type=float, default=0.9, help="Train/test split ratio, default is 0.9.")
    split_parser.add_argument("--seed", type=int, default=42, help="Seed for dataset shuffling.")

    # global arguments
    split_parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
    # endregion

    # region DATASET STATISTICS ARGUMENTS
    stats_parser = subparsers.add_parser("stats")
    stats_parser.add_argument("image_dir", help="Path to images.")
    stats_parser.add_argument("annot_dir", help="Path to annotations.")

    stats_parser.add_argument("-o", "--output_dir", type=str, default=None, help="If used, plots will be saved here.")
    stats_parser.add_argument("-i", "--input_format", default=InputFormat.MUNG.value,
                              choices=InputFormat.get_all_value())
    stats_parser.add_argument('-j', '--jobs', nargs='+', help="Specify jobs to run, if None, all jobs will be run.",
                              choices=StatJob.get_all_value())

    stats_parser.add_argument("--image_format", default="jpg", help="Input image format.")

    # global arguments
    stats_parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
    stats_parser.add_argument("--config", default=None,
                              help="Path to config, see \"default.config\" for example.")
    stats_parser.add_argument("--sum", action="store_true", help="Adds \"All\" category to stats.")
    # endregion

    # region MODEL VALIDATION ARGUMENTS
    val_parser = subparsers.add_parser("val")

    val_parser.add_argument("model_path", type=str, help="Path to model.")
    val_parser.add_argument("image_dir", help="Path to images.")
    val_parser.add_argument("annot_dir", help="Path to annotations.")

    val_parser.add_argument("-i", "--input_format", default=InputFormat.MUNG.value,
                            choices=InputFormat.get_all_value())
    val_parser.add_argument("-m", "--model_type", default="yolod", choices=["yolod", "yolos"],
                            help="Type of model.")

    val_parser.add_argument("-o", "--output_dir", type=str, default=None,
                            help="Path to output directory, if not specified, plot will be shown.")

    val_parser.add_argument("--image_format", default="jpg", help="Input image format.")

    val_parser.add_argument("--overlap", type=float, default=0.25, help="Overlap ratio for image splits.")
    val_parser.add_argument("-c", "--count", type=int, help="How many images the model will be tested on.")
    val_parser.add_argument("-s", "--seed", type=int, default=42, help="Seed for dataset shuffling.")
    val_parser.add_argument("--sum", action="store_true", help="Adds \"All\" category to evaluation.")
    val_parser.add_argument("--iou", type=float, default=0.25,
                            help="Threshold to consider two annotations overlapping while resolving predictions.")

    # global arguments
    val_parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
    val_parser.add_argument("--config", default=None,
                            help="Path to config, see \"default.config\" for example.")

    # endregion

    # region CONFIG CHECK ARGUMENTS
    conf_parser = subparsers.add_parser("confcheck")
    conf_parser.add_argument("config_path", help="Path to config.")
    # endregion

    # region DEFAULT RESOURCES UPDATE
    update_parser = subparsers.add_parser("update")
    # endregion

    # region K-FOLD ARGUMENTS
    kfold_parser = subparsers.add_parser("kfold")
    kfold_parser.add_argument("output", help="Split dataset destination.")
    kfold_parser.add_argument("image_dir", help="Path to images.")
    kfold_parser.add_argument("annot_dir", help="Path to annotations.")
    kfold_parser.add_argument("-f", "--folds", type=int, default=3, help="Number of folds.")
    kfold_parser.add_argument("-p", "--pout", type=int, default=1, help="Leave p out.")

    # global arguments
    kfold_parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")
    kfold_parser.add_argument("--seed", type=int, default=42, help="Seed for dataset shuffling.")
    # endregion

    args = parser.parse_args()

    # CONFIG VERBOSE CHECK
    if args.command == "confcheck":
        with open(args.config_path, "r", encoding="utf8") as f:
            loaded_config = json.load(f)

        Utils.get_mapping_and_names_from_config(loaded_config, verbose=True)
        return 0

    # DATASET TRAIN/TEST SPLIT (without any augmentation or image splitting)
    if args.command == "split":
        Formatter.split_and_save_dataset(
            # directories
            Path(args.output),
            Path(args.image_dir),
            Path(args.annot_dir),

            split_ratio=args.split,
            seed=args.seed,
            verbose=args.verbose
        )
        return 0

    # UPDATE RESOURCES
    elif args.command == "update":
        from .Download import update_all_default_resources
        update_all_default_resources()
        return 0

    # RUN K-FOLD ON DATASET
    elif args.command == "kfold":
        from .KFold import kfold_dataset
        kfold_dataset(
            Path(args.output),
            Path(args.image_dir),
            Path(args.annot_dir),
            folds=args.folds,
            pout=args.pout,
            seed=args.seed,
            verbose=args.verbose
        )
        return 0

    # CONFIG LOADING
    # later methods need the config loaded
    if args.config is None:
        with open("configs/default.json", "rt") as f:
            loaded_config = json.load(f)
    else:
        with open(args.config, "r", encoding="utf8") as f:
            loaded_config = json.load(f)

    class_id_mapping, class_output_names = Utils.get_mapping_and_names_from_config(loaded_config)

    # DATASET FORMATTING
    if args.command == "form":
        # input preprocessing
        input_f = InputFormat.from_string(args.input_format)
        output_f = OutputFormat.from_string(args.output_format)

        if not args.image_splitting and args.augmentation is not None:
            raise ValueError("Cannot augment data without image splitting")

        if args.augmentation is not None:
            args.augmentation = [float(a) for a in args.augmentation]

            if 1.0 not in args.augmentation:
                print("Warning: Adding 1.0 to augmentation ratios")
                args.augmentation.append(1.0)

            args.augmentation = sorted(args.augmentation)

            if args.verbose:
                print(f"Augmentation ratios: {args.augmentation}")

        Formatter.format_dataset(
            # directories
            Path(args.output),
            Path(args.image_dir),
            Path(args.annot_dir),
            # class ids etc.
            class_reference_table=class_id_mapping,
            class_output_names=class_output_names,
            # formatting
            input_format=input_f,
            output_format=output_f,
            split_ratio=args.split,
            resize=args.resize,
            image_format=args.image_format,
            # image splitting settings
            window_size=(loaded_config["window_size"][0], loaded_config["window_size"][1]),
            overlap_ratio=loaded_config["overlap_ratio"],
            image_splitting=args.image_splitting,
            # augmentation
            aug_ratios=args.augmentation,
            # others
            seed=args.seed,
            verbose=args.verbose
        )
    # DATASET STATISTICS
    elif args.command == "stats":
        Plots.load_and_plot_stats(
            # directories
            Path(args.image_dir),
            Path(args.annot_dir),
            InputFormat.from_string(args.input_format),
            # class ids etc.
            class_reference_table=class_id_mapping,
            class_output_names=class_output_names,
            image_format=args.image_format,
            jobs=[StatJob.from_string(job) for job in args.jobs] if args.jobs else None,
            # others
            output_dir=Path(args.output_dir) if args.output_dir is not None else None,
            summarize=args.sum,
            verbose=args.verbose
        )
    # MODEL VALIDATION
    elif args.command == "val":
        EvalJob.run_f1_scores_vs_iou(
            # input paths
            Path(args.model_path),
            Path(args.image_dir),
            Path(args.annot_dir),
            # formatting
            InputFormat.from_string(args.input_format),
            EvalJob.ModelType.from_string(args.model_type),
            class_output_names,
            iou_threshold=args.iou,
            overlap=args.overlap,
            # optional graph saving
            output_dir=Path(args.output_dir) if args.output_dir is not None else None,
            summarize=args.sum,
            count=args.count,
            verbose=args.verbose
        )


if __name__ == "__main__":
    main()
