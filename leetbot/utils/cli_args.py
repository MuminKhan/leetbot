import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--channel",
        "-c",
        required=True,
        dest="channel",
        action="store",
        help="Channel to post to. Bot must be a member to post.",
    )
    parser.add_argument(
        "--alert", required=False, dest="alert", action="store_true", help="Whether or not to send an @channel alert."
    )
    parser.add_argument(
        "--data_file",
        "-D",
        required=False,
        dest="data_file",
        action="store",
        help='Where to read/write posted questions. Default="./leetbot.json"',
        default="leetbot.json",
    )
    parser.add_argument(
        "--difficulty",
        "-d",
        required=False,
        dest="difficulty",
        action="store",
        help="List of any combination of [easy, medium, hard]",
        type=str,
        default="easy,medium,hard",
    )

    args = parser.parse_args()
    args.difficulty = args.difficulty.lower()

    print("Args:")
    [print(f"\t{k}: {v}") for k, v in args.__dict__.items()]

    return args
