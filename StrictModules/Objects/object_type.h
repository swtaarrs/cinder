// Copyright (c) Facebook, Inc. and its affiliates. (http://www.facebook.com)
#ifndef __STRICTM_OBJECT_TYPE_H__
#define __STRICTM_OBJECT_TYPE_H__

#include "StrictModules/Objects/type.h"

namespace strictmod::objects {

class StrictObjectType : public StrictType {
 public:
  using StrictType::StrictType;

  virtual std::shared_ptr<BaseStrictObject> getDescr(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> inst,
      std::shared_ptr<StrictType> type,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> setDescr(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> inst,
      std::shared_ptr<BaseStrictObject> value,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> delDescr(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> inst,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> loadAttr(
      std::shared_ptr<BaseStrictObject> obj,
      const std::string& key,
      std::shared_ptr<BaseStrictObject> defaultValue,
      const CallerContext& caller) override;

  virtual void storeAttr(
      std::shared_ptr<BaseStrictObject> obj,
      const std::string& key,
      std::shared_ptr<BaseStrictObject> value,
      const CallerContext& caller) override;

  virtual void delAttr(
      std::shared_ptr<BaseStrictObject> obj,
      const std::string& key,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> binOp(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> right,
      operator_ty op,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> reverseBinOp(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> left,
      operator_ty op,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> unaryOp(
      std::shared_ptr<BaseStrictObject> obj,
      unaryop_ty op,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> binCmpOp(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> right,
      cmpop_ty op,
      const CallerContext& caller) override;

  virtual std::shared_ptr<StrictIteratorBase> getElementsIter(
      std::shared_ptr<BaseStrictObject> obj,
      const CallerContext& caller) override;

  virtual std::vector<std::shared_ptr<BaseStrictObject>> getElementsVec(
      std::shared_ptr<BaseStrictObject> obj,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> getElement(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> index,
      const CallerContext& caller) override;

  virtual void setElement(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> index,
      std::shared_ptr<BaseStrictObject> value,
      const CallerContext& caller) override;

  virtual void delElement(
      std::shared_ptr<BaseStrictObject> obj,
      std::shared_ptr<BaseStrictObject> index,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> call(
      std::shared_ptr<BaseStrictObject> obj,
      const std::vector<std::shared_ptr<BaseStrictObject>>& args,
      const std::vector<std::string>& argNames,
      const CallerContext& caller) override;

  virtual std::shared_ptr<BaseStrictObject> getTruthValue(
      std::shared_ptr<BaseStrictObject> obj,
      const CallerContext& caller) override;

  virtual std::unique_ptr<BaseStrictObject> constructInstance(
      std::shared_ptr<StrictModuleObject> caller) override;
};
} // namespace strictmod::objects

#endif //__STRICTM_OBJECT_TYPE_H__
