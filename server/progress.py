import _thread

from stringcase import camelcase


def case(s: str, to_camel: bool = False):
    if to_camel:
        return camelcase(s)
    return s


def done(instance, prefix: str, callback: callable = None):
    def wrapped():
        setattr(instance, "{}ed".format(prefix), True)
        setattr(instance, "{}ing".format(prefix), False)
        if callback is not None:
            callback()

    return wrapped


def update(instance, classifiers, force: bool = False):
    _, outdated_classifier_ids = instance.outdated()
    if force:
        classifiers.evaluate_all(instance.search_id, update=force)
    else:
        for classifier_id in outdated_classifier_ids:
            classifiers.evaluate(instance.search_id, classifier_id, no_threading=True)
    instance.is_computed = True
    instance.is_computed = False


class Progress:
    def __init__(
        self,
        search_id: int,
        classifier_ids,
        unpredictability_all,
        unpredictability_labels,
        prediction_proba_change_all,
        prediction_proba_change_labels,
        convergence_all,
        convergence_labels,
        divergence_all,
        divergence_labels,
        num_labels,
    ):
        self.search_id = search_id

        self.classifier_ids = classifier_ids
        self.unpredictability_all = unpredictability_all
        self.unpredictability_labels = unpredictability_labels
        self.prediction_proba_change_all = prediction_proba_change_all
        self.prediction_proba_change_labels = prediction_proba_change_labels
        self.convergence_all = convergence_all
        self.convergence_labels = convergence_labels
        self.divergence_all = divergence_all
        self.divergence_labels = divergence_labels
        self.num_labels = num_labels

        is_outdated, outdated_classifier_ids = self.outdated()

        self.is_computed = not is_outdated
        self.is_computing = False

        self.outdated_classifier_ids = outdated_classifier_ids

    def update(self, classifiers, force: bool = False):
        if self.is_computing:
            return

        self.is_computed = False
        self.is_computing = True
        print("-------------------------------------------", force)
        try:
            _thread.start_new_thread(update, (self, classifiers, force))
        except Exception:
            self.is_computed = False
            self.is_computing = False

    def outdated(self):
        if len(self.unpredictability_all) == 0:
            return False, []

        is_outdated = False
        outdated = []
        for i in range(len(self.unpredictability_all)):
            if self.unpredictability_all[i] is None:
                is_outdated = True
                outdated.append(i)

        return is_outdated, outdated

    def to_dict(self, camel_case: bool = False):
        out = {}

        unpredictability_all = None
        unpredictability_labels = None
        prediction_proba_change_all = None
        prediction_proba_change_labels = None
        convergence_all = None
        convergence_labels = None
        divergence_all = None
        divergence_labels = None

        if self.is_computed:
            unpredictability_all = self.unpredictability_all
            unpredictability_labels = self.unpredictability_labels
            prediction_proba_change_all = self.prediction_proba_change_all
            prediction_proba_change_labels = self.prediction_proba_change_labels
            convergence_all = self.convergence_all
            convergence_labels = self.convergence_labels
            divergence_all = self.divergence_all
            divergence_labels = self.divergence_labels

        out[case("search_id", camel_case)] = self.search_id
        out[case("is_computed", camel_case)] = self.is_computed
        out[case("is_computing", camel_case)] = self.is_computing
        out[case("num_labels", camel_case)] = self.num_labels
        out[case("unpredictability_all", camel_case)] = unpredictability_all
        out[case("unpredictability_labels", camel_case)] = unpredictability_labels
        out[
            case("prediction_proba_change_all", camel_case)
        ] = prediction_proba_change_all
        out[
            case("prediction_proba_change_labels", camel_case)
        ] = prediction_proba_change_labels
        out[case("convergence_all", camel_case)] = convergence_all
        out[case("convergence_labels", camel_case)] = convergence_labels
        out[case("divergence_all", camel_case)] = divergence_all
        out[case("divergence_labels", camel_case)] = divergence_labels

        return out