#include "ilqr.h"

int main()
{
    auto x = casadi::SX::sym("x", 1);
    auto u = casadi::SX::sym("u", 1);
    auto p = casadi::SX::sym("p", 1);
    auto dt = casadi::SX::sym("dt", 1);
    auto f = casadi::Function("f", {x, u, dt}, {x + dt*u}, {"x", "u", "dt"}, {"f"});
    auto l = casadi::Function("l", {x, u}, {casadi::SX::sumsqr(u)*1e-6}, {"x", "u"}, {"l"});
    auto lf = casadi::Function("l", {x, u}, {casadi::SX::sumsqr(x)*0.5}, {"x", "u"}, {"l"});
    auto cf = casadi::Function("h", {x, u, p}, {x - p}, {"x", "u", "myparam"}, {"h"});

    int N = 3;
    horizon::IterativeLQR ilqr(f, N);

    Eigen::MatrixXd xlb, xub;
    xlb.setConstant(1, N+1, -INFINITY);
    xub.setConstant(1, N+1, INFINITY);
    xlb(N) = 1.0;
    xub(N) = 1.0;
    ilqr.setStateBounds(xlb, xub);

    Eigen::MatrixXd ulb, uub;
    ulb.setConstant(1, N, -INFINITY);
    uub.setConstant(1, N, INFINITY);
    ulb(0) = 11.0;
    uub(0) = 11.0;
    ilqr.setInputBounds(ulb, uub);

    Eigen::VectorXd x0(1);
    x0 << 0.0;
    ilqr.setInitialState(x0);
    xlb(0) = x0(0);
    xub(0) = x0(0);

    ilqr.setCost({0, 1}, l);
    ilqr.setConstraint({2}, cf);

    Eigen::MatrixXd myparam_values;
    myparam_values.setConstant(1, N+1, -1.0);
    ilqr.setParameterValue("myparam", myparam_values);

    Eigen::MatrixXd dt_values;
    dt_values.setConstant(1, N+1, 0.1);
    ilqr.setParameterValue("dt", dt_values);

    ilqr.solve(10);

    std::cout << ilqr.getStateTrajectory() << std::endl;
    std::cout << ilqr.getInputTrajectory() << std::endl;
}
