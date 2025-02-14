set(LLVM_LINK_COMPONENTS support FrontendOpenMP)

add_clang_library(clangToolingRefactor
  ASTSlice.cpp
  ASTStateSerialization.cpp
  Extract.cpp
  ExtractRepeatedExpressionIntoVariable.cpp
  ExtractionUtils.cpp
  FillInEnumSwitchCases.cpp
  FillInMissingMethodStubsFromAbstractClasses.cpp
  FillInMissingProtocolStubs.cpp
  IfSwitchConversion.cpp
  ImplementDeclaredMethods.cpp
  IndexerQueries.cpp
  LocalizeObjCStringLiteral.cpp
  RefactoringActions.cpp
  RefactoringActionFinder.cpp
  RefactoringOperation.cpp
  RefactoringOptions.cpp
  RenamingOperation.cpp
  RenameIndexedFile.cpp
  RenamedSymbol.cpp
  SourceLocationUtilities.cpp
  StmtUtils.cpp
  SymbolOperation.cpp
  SymbolOccurrenceFinder.cpp
  SymbolUSRFinder.cpp
  TypeUtils.cpp
  USRFinder.cpp

  DEPENDS
  ClangDriverOptions

  LINK_LIBS
  clangAST
  clangASTMatchers
  clangBasic
  clangEdit
  clangFrontend
  clangIndex
  clangLex
  clangToolingCore
  clangRewrite
  )

if(CMAKE_SYSTEM_NAME STREQUAL Windows)
  set_source_files_properties(Extract.cpp PROPERTIES COMPILE_FLAGS /bigobj)
endif()
