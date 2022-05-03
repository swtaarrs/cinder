// Copyright (c) Facebook, Inc. and its affiliates. (http://www.facebook.com)
#pragma once

#include "Jit/hir/hir.h"

#include <json.hpp>

#include <iostream>
#include <sstream>
#include <string>

namespace jit {
namespace hir {

enum PrinterFlags {
  kNone = 0,
  kShowSnapshots = 0x1 << 0,
  kShowLineNumbers = 0x1 << 1,
};

// Helper class for pretty printing IR
//
// TODO(mpage): This works, but feels horribly kludgy. This should be possible
// using a custom streambuf for indentation and via overloads for <<.
class HIRPrinter {
 public:
  explicit HIRPrinter(
      PrinterFlags flags = PrinterFlags::kNone,
      const std::string line_prefix = "")
      : show_snapshots_(flags & PrinterFlags::kShowSnapshots),
        show_line_numbers_(flags & PrinterFlags::kShowLineNumbers),
        line_prefix_(line_prefix) {}

  void Print(std::ostream& os, const Function& func);
  void Print(std::ostream& os, const CFG& cfg);
  void Print(std::ostream& os, const BasicBlock& block);
  void Print(std::ostream& os, const Instr& instr);
  void Print(std::ostream& os, const FrameState& state);
  void Print(std::ostream& os, const CFG& cfg, BasicBlock* start);

  template <class T>
  std::string ToString(const T& obj) {
    std::ostringstream os;
    Print(os, obj);
    return os.str();
  }

  template <class T>
  void Print(const T& obj) {
    Print(std::cout, obj);
  }

 private:
  void PrintLineNumber(std::ostream& os, int line, const char* filename);
  void Indent();
  void Dedent();
  std::ostream& Indented(std::ostream& os);

  int indent_level_{0};
  bool show_snapshots_{false};
  bool show_line_numbers_{false};
  std::string line_prefix_;
};

// TODO(emacs): Handle no PyCodeObject
class JSONPrinter {
 public:
  nlohmann::json PrintSource(const Function& func);
  nlohmann::json PrintBytecode(const Function& func);
  void Print(
      nlohmann::json& passes,
      const Function& func,
      const char* pass_name,
      std::size_t time_ns);
  nlohmann::json Print(const CFG& cfg);
  nlohmann::json Print(const BasicBlock& instr);
  nlohmann::json Print(const Instr& instr);
};

inline PrinterFlags getFlags() {
  PrinterFlags result = PrinterFlags::kNone;
  if (g_dump_hir_line_numbers) {
    result = static_cast<PrinterFlags>(result | PrinterFlags::kShowLineNumbers);
  }
  return result;
}

inline std::ostream& operator<<(std::ostream& os, const Function& func) {
  HIRPrinter(getFlags()).Print(os, func);
  return os;
}

inline std::ostream& operator<<(std::ostream& os, const CFG& cfg) {
  HIRPrinter(getFlags()).Print(os, cfg);
  return os;
}

inline std::ostream& operator<<(std::ostream& os, const BasicBlock& block) {
  HIRPrinter(getFlags()).Print(os, block);
  return os;
}

inline std::ostream& operator<<(std::ostream& os, const Instr& instr) {
  HIRPrinter(getFlags()).Print(os, instr);
  return os;
}

inline std::ostream& operator<<(std::ostream& os, const FrameState& state) {
  HIRPrinter(getFlags()).Print(os, state);
  return os;
}

void DebugPrint(const CFG& cfg);
void DebugPrint(const BasicBlock& block);
void DebugPrint(const Instr& instr);

} // namespace hir
} // namespace jit
