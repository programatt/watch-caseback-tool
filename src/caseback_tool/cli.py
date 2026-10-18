"""Command line interface."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from . import __version__
from .geometry import (
    DiskSpec,
    HandleSpec,
    disk_scad,
    export_stl,
    handle_scad,
    png_to_jpg,
    render_stl_png,
    write_scad,
)


SKX_EXAMPLE = DiskSpec(
    notch_circle_diameter=31.0,
    notch_count=6,
    notch_depth=1.2,
    notch_length=1.6,
    notch_width=2.4,
    disk_diameter=34.6,
)


def _add_output(parser: argparse.ArgumentParser, default: str) -> None:
    parser.add_argument("-o", "--output", type=Path, default=Path(default), help="output STL path")
    parser.add_argument(
        "--scad-only",
        action="store_true",
        help="write the parametric .scad source but do not invoke OpenSCAD",
    )


def _disk_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("disk", help="generate a case-back opening disk")
    parser.add_argument("--notch-circle-diameter", type=float, required=True, metavar="MM")
    parser.add_argument("--notch-count", type=int, required=True)
    parser.add_argument("--notch-depth", type=float, required=True, metavar="MM")
    parser.add_argument("--notch-length", type=float, required=True, metavar="MM")
    parser.add_argument("--notch-width", type=float, required=True, metavar="MM")
    parser.add_argument("--disk-diameter", type=float, metavar="MM")
    parser.add_argument("--body-thickness", type=float, default=5.0, metavar="MM")
    parser.add_argument("--drive-af", type=float, default=12.0, metavar="MM")
    parser.add_argument("--drive-height", type=float, default=7.0, metavar="MM")
    parser.add_argument("--insert-diameter", type=float, default=5.6, metavar="MM")
    parser.add_argument("--insert-depth", type=float, default=5.5, metavar="MM")
    parser.add_argument("--facets", type=int, default=128)
    _add_output(parser, "caseback_disk.stl")


def _handle_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("handle", help="generate the reusable locking handle")
    parser.add_argument("--handle-length", type=float, default=130.0, metavar="MM")
    parser.add_argument("--handle-width", type=float, default=24.0, metavar="MM")
    parser.add_argument("--handle-thickness", type=float, default=12.0, metavar="MM")
    parser.add_argument("--drive-af", type=float, default=12.0, metavar="MM")
    parser.add_argument("--drive-height", type=float, default=7.0, metavar="MM")
    parser.add_argument("--fit-clearance", type=float, default=0.25, metavar="MM")
    parser.add_argument("--screw-clearance", type=float, default=4.5, metavar="MM")
    parser.add_argument("--screw-head-diameter", type=float, default=8.0, metavar="MM")
    parser.add_argument("--screw-head-depth", type=float, default=3.4, metavar="MM")
    parser.add_argument("--facets", type=int, default=128)
    _add_output(parser, "caseback_handle.stl")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="caseback-tool",
        description="Generate printable watch case-back opening disks and a reusable handle.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)
    _disk_parser(subparsers)
    _handle_parser(subparsers)
    example = subparsers.add_parser(
        "skx-example", help="generate the documented Seiko SKX fit-check example and renders"
    )
    example.add_argument("--output-dir", type=Path, default=Path("skx-example"))
    return parser


def _scad_path(stl_path: Path) -> Path:
    return stl_path.with_suffix(".scad")


def _write_disk(args: argparse.Namespace) -> list[Path]:
    spec = DiskSpec(
        notch_circle_diameter=args.notch_circle_diameter,
        notch_count=args.notch_count,
        notch_depth=args.notch_depth,
        notch_length=args.notch_length,
        notch_width=args.notch_width,
        disk_diameter=args.disk_diameter,
        body_thickness=args.body_thickness,
        drive_af=args.drive_af,
        drive_height=args.drive_height,
        insert_diameter=args.insert_diameter,
        insert_depth=args.insert_depth,
        facets=args.facets,
    )
    scad = write_scad(_scad_path(args.output), disk_scad(spec))
    outputs = [scad]
    if not args.scad_only:
        outputs.append(export_stl(scad, args.output))
    return outputs


def _write_handle(args: argparse.Namespace) -> list[Path]:
    spec = HandleSpec(
        handle_length=args.handle_length,
        handle_width=args.handle_width,
        handle_thickness=args.handle_thickness,
        drive_af=args.drive_af,
        drive_height=args.drive_height,
        fit_clearance=args.fit_clearance,
        screw_clearance=args.screw_clearance,
        screw_head_diameter=args.screw_head_diameter,
        screw_head_depth=args.screw_head_depth,
        facets=args.facets,
    )
    scad = write_scad(_scad_path(args.output), handle_scad(spec))
    outputs = [scad]
    if not args.scad_only:
        outputs.append(export_stl(scad, args.output))
    return outputs


def _write_example(output_dir: Path) -> list[Path]:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    disk_scad_path = write_scad(output_dir / "skx_caseback_disk.scad", disk_scad(SKX_EXAMPLE))
    handle_spec = HandleSpec()
    handle_scad_path = write_scad(output_dir / "caseback_handle.scad", handle_scad(handle_spec))
    outputs = [
        disk_scad_path,
        export_stl(disk_scad_path, output_dir / "skx_caseback_disk.stl"),
        handle_scad_path,
        export_stl(handle_scad_path, output_dir / "caseback_handle.stl"),
    ]

    disk_png = render_stl_png(
        output_dir / "skx_caseback_disk.stl",
        output_dir / "skx_caseback_disk.png",
        "disk",
        SKX_EXAMPLE.notch_depth + SKX_EXAMPLE.body_thickness + SKX_EXAMPLE.drive_height,
    )
    handle_png = render_stl_png(
        output_dir / "caseback_handle.stl",
        output_dir / "caseback_handle.png",
        "handle",
        handle_spec.handle_thickness,
        image_size=(1400, 800),
    )
    outputs.extend(
        [
            png_to_jpg(disk_png, output_dir / "skx_caseback_disk.jpg"),
            png_to_jpg(handle_png, output_dir / "caseback_handle.jpg"),
        ]
    )
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "disk":
            outputs = _write_disk(args)
        elif args.command == "handle":
            outputs = _write_handle(args)
        else:
            outputs = _write_example(args.output_dir)
    except (ValueError, RuntimeError, OSError) as error:
        parser.exit(2, f"error: {error}\n")
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
