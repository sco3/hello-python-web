#!/usr/bin/env -S cargo run
// --bin process-outputs

use std::collections::BTreeMap;
use std::env;
use std::fs::File;
use std::io;
use std::io::BufRead;
use std::path::Path;

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();

    if args.is_empty() {
        eprintln!("Usage: cargo run <file1> <file2> ...");
        return ();
    }

    let mut results: BTreeMap<i64, i64> = BTreeMap::new();

    for file_path in args.into_iter() {
        if file_path.ends_with(".rs") {
            continue;
        }
        let size_str = file_path.split('.').nth(3);
        if let Some(size_str) = size_str {
            let size = size_str.parse().unwrap_or_default();

            let path = Path::new(&file_path);

            if !path.exists() {
                eprintln!("File not found: {}", file_path);
                continue;
            }

            match File::open(&path) {
                Ok(file) => {
                    let reader = io::BufReader::new(file);
                    let mut msg_per_sec: i64 = i64::MAX;
                    for line in reader.lines() {
                        if let Ok(line) = line {
                            let stat: f64 = line.trim().parse().unwrap_or_default();
                            let rounded = stat.ceil() as i64;
                            if rounded < msg_per_sec {
                                msg_per_sec = rounded
                            }
                        }
                    }
                    if size > 0 {
                        results.insert(size, msg_per_sec);
                    }
                }
                Err(err) => {
                    eprintln!("Error opening file {}: {}", file_path, err);
                }
            }
        }
    }
    println!("\"Message size\" , \"msg/s\"");
    for (key, value) in results {
        println!("{} , {}", key, value);
    }
}