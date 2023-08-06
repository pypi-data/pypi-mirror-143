import pharmpy.results
import pharmpy.tools.iiv.algorithms as algorithms
import pharmpy.tools.modelsearch.tool
from pharmpy.modeling import (
    add_iiv,
    copy_model,
    create_joint_distribution,
    summarize_modelfit_results,
    update_inits,
)
from pharmpy.tools.modelfit import create_fit_workflow
from pharmpy.workflows import Task, Workflow


def create_workflow(
    algorithm,
    add_iivs=False,
    iiv_as_fullblock=False,
    rankfunc='bic',
    cutoff=None,
    model=None,
):
    algorithm_func = getattr(algorithms, algorithm)

    # FIXME: must currently be a model, cannot be a task
    if add_iivs:
        model_iiv = copy_model(model, f'{model.name}_add_iiv')
        _add_iiv(iiv_as_fullblock, model_iiv)
        iivs = model_iiv.random_variables.iiv
    else:
        iivs = model.random_variables.iiv

    wf = Workflow()
    wf.name = 'iiv'

    start_task = Task('start_iiv', start, add_iivs, iiv_as_fullblock, model)
    wf.add_task(start_task)

    if not model.modelfit_results or add_iivs:
        wf_fit = create_fit_workflow(n=1)
        wf.insert_workflow(wf_fit)
        start_model_task = wf_fit.output_tasks
    else:
        start_model_task = [start_task]

    task_update_inits = Task('update_inits_start_model', _update_inits_start_model)
    wf.add_task(task_update_inits, predecessors=wf.output_tasks)

    wf_method, model_features = algorithm_func(iivs)
    wf.insert_workflow(wf_method)

    task_result = Task(
        'results',
        post_process_results,
        rankfunc,
        cutoff,
        model_features,
    )

    wf.add_task(task_result, predecessors=start_model_task + wf.output_tasks)

    return wf


def start(add_iivs, iiv_as_fullblock, model):
    if add_iivs:
        model = copy_model(model, f'{model.name}_add_iiv')
        _add_iiv(iiv_as_fullblock, model)
    return model


def _add_iiv(iiv_as_fullblock, model):
    sset, rvs = model.statements, model.random_variables
    odes = sset.ode_system

    params_to_add_etas = []

    for param in odes.free_symbols:
        assign = sset.find_assignment(param)
        if assign:
            if _has_iiv(sset, rvs, assign):
                continue
            dep_assignments = _get_dependent_assignments(sset, assign)
            if dep_assignments:
                for dep_assign in dep_assignments:
                    param_name = dep_assign.symbol.name
                    if not _has_iiv(sset, rvs, dep_assign) and param_name not in params_to_add_etas:
                        params_to_add_etas.append(param_name)
            else:
                if param.name not in params_to_add_etas:
                    params_to_add_etas.append(param.name)

    if params_to_add_etas:
        add_iiv(model, params_to_add_etas, 'exp')

    if iiv_as_fullblock:
        create_joint_distribution(model)
    return model


def _get_dependent_assignments(sset, assignment):
    # Finds dependant assignments one layer deep
    dep_assignments = [sset.find_assignment(symb) for symb in assignment.expression.free_symbols]
    return list(filter(None, dep_assignments))


def _has_iiv(sset, rvs, assignment):
    full_expression = sset.before_odes.full_expression(assignment.symbol)
    symb_names = {symb.name for symb in full_expression.free_symbols}
    if symb_names.intersection(rvs.iiv.names):
        return True
    return False


def _update_inits_start_model(model):
    try:
        update_inits(model)
    except ValueError:
        pass
    return model


def post_process_results(rankfunc, cutoff, model_features, *models):
    start_model, res_models = models

    if isinstance(res_models, tuple):
        res_models = list(res_models)
    else:
        res_models = [res_models]

    summary_tool = pharmpy.tools.modelsearch.tool.create_summary(
        res_models,
        start_model,
        rankfunc,
        cutoff,
        model_features,
        rank_by_not_worse=True,
        bic_type='iiv',
    )

    best_model_name = summary_tool['rank'].idxmin()
    try:
        best_model = [model for model in res_models if model.name == best_model_name][0]
    except IndexError:
        best_model = start_model

    summary_models = summarize_modelfit_results([start_model] + res_models)

    res = IIVResults(
        summary_tool=summary_tool,
        summary_models=summary_models,
        best_model=best_model,
        start_model=start_model,
        models=res_models,
    )

    return res


class IIVResults(pharmpy.results.Results):
    def __init__(
        self, summary_tool=None, summary_models=None, best_model=None, start_model=None, models=None
    ):
        self.summary_tool = summary_tool
        self.summary_models = summary_models
        self.best_model = best_model
        self.start_model = start_model
        self.models = models
