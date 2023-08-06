// This file is part of sen-py <https://github.com/senpy-club/sen-py>.
// Copyright (C) 2022-2022 Fuwn <contact@fuwn.me>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, version 3.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.
//
// Copyright (C) 2022-2022 Fuwn <contact@fuwn.me>
// SPDX-License-Identifier: GPL-3.0-only

#![deny(
  warnings,
  nonstandard_style,
  unused,
  future_incompatible,
  rust_2018_idioms,
  unsafe_code
)]
#![deny(clippy::all, clippy::nursery, clippy::pedantic)]
#![recursion_limit = "128"]
#![allow(clippy::use_self)]

use pyo3::{exceptions::PyValueError, prelude::*};

const SENPY_CLUB_API_BASE_URL: &str = senpy::SENPY_CLUB_API_BASE_URL;
const SENPY_CLUB_API_CURRENT_VERSION: u32 =
  senpy::SENPY_CLUB_API_CURRENT_VERSION;
const SENPY_CLUB_API_URL: &str = senpy::SENPY_CLUB_API_URL;

#[pyclass]
#[allow(unused)]
struct Random {
  #[pyo3(get)]
  language: String,
  #[pyo3(get)]
  image:    String,
}
#[pymethods]
impl Random {
  #[new]
  fn py_new() -> PyResult<Self> {
    match senpy::random() {
      Ok(image) =>
        Ok(Self {
          language: image.language,
          image:    image.image,
        }),
      Err(e) => Err(PyValueError::new_err(e.to_string())),
    }
  }
}

/// If all is good with no errors; returns a `Vec` of languages
///
/// # Errors
/// if The Senpy Club API is unavailable
#[pyfunction]
pub fn languages() -> PyResult<Vec<String>> {
  match senpy::languages() {
    Ok(languages) => Ok(languages),
    Err(e) => Err(PyValueError::new_err(e.to_string())),
  }
}

/// If all is good with no errors; returns a `Vec` of images of language
/// `language`
///
/// # Errors
/// if The Senpy Club API is unavailable
#[pyfunction]
#[allow(clippy::needless_pass_by_value)]
pub fn language(language: String) -> PyResult<Vec<String>> {
  match senpy::language(&language) {
    Ok(languages) => Ok(languages),
    Err(e) => Err(PyValueError::new_err(e.to_string())),
  }
}

/// If all is good with no errors; returns `true` if live, returns `false` if
/// down.
///
/// # Errors
/// if `reqwest` cannot send the request to The Senpy API
#[pyfunction]
pub fn status() -> PyResult<bool> {
  match senpy::status() {
    Ok(status) => Ok(status),
    Err(e) => Err(PyValueError::new_err(e.to_string())),
  }
}

#[pymodule]
fn senpy_club(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
  module.add("SENPY_CLUB_API_BASE_URL", SENPY_CLUB_API_BASE_URL)?;
  module.add(
    "SENPY_CLUB_API_CURRENT_VERSION",
    SENPY_CLUB_API_CURRENT_VERSION,
  )?;
  module.add("SENPY_CLUB_API_URL", SENPY_CLUB_API_URL)?;
  module.add_class::<Random>()?;
  module.add_function(wrap_pyfunction!(languages, module)?)?;
  module.add_function(wrap_pyfunction!(language, module)?)?;
  module.add_function(wrap_pyfunction!(status, module)?)?;

  Ok(())
}
