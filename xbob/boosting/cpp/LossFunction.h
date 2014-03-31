#ifndef XBOB_BOOSTING_LOSS_FUNCTION_H
#define XBOB_BOOSTING_LOSS_FUNCTION_H

#include <blitz/array.h>

class LossFunction{
  public:
    void lossSum(const blitz::Array<double,1>& alpha, const blitz::Array<double,2>& targets, const blitz::Array<double,2>& previous_scores, const blitz::Array<double,2>& current_scores, blitz::Array<double,1>& loss_sum) const;
    void gradientSum(const blitz::Array<double,1>& alpha, const blitz::Array<double,2>& targets, const blitz::Array<double,2>& previous_scores, const blitz::Array<double,2>& current_scores, blitz::Array<double,1>& gradient_sum) const;

    virtual void loss(const blitz::Array<double, 2>& targets, const blitz::Array<double, 2>& scores, blitz::Array<double, 2>& errors) const = 0;
    virtual void lossGradient(const blitz::Array<double, 2>& targets, const blitz::Array<double, 2>& scores, blitz::Array<double, 2>& gradient) const = 0;

  protected:
    // This class is not instantiatable
    LossFunction(){}

  private:
    mutable blitz::Array<double,2> scores;
    mutable blitz::Array<double,2> errors;
    mutable blitz::Array<double,2> gradients;
};

#endif // XBOB_BOOSTING_LOSS_FUNCTION_H
