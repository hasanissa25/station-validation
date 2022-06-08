from typing import Any, List
import warnings
warnings.filterwarnings("ignore")


class Attachments(dict):
    @property
    def failed_latencies(self) -> List[Any]:
        return self["failed_latencies"]

    @property
    def latency_line_plot(self) -> List[Any]:
        return self["latency_line_plot"]

    @property
    def latency_log_plot(self) -> List[Any]:
        return self["latency_log_plot"]

    @property
    def timely_availability_plot(self) -> List[Any]:
        return self["timely_availability_plot"]

    @property
    def timing_error(self) -> List[Any]:
        return self["timing_error"]

    @property
    def timing_quality(self) -> List[Any]:
        return self["timing_quality"]

    @property
    def validation_results(self) -> List[Any]:
        return self["validation_results"]

    @property
    def adc_count(self) -> List[Any]:
        return self["adc_count"]

    @property
    def max_gap(self) -> List[Any]:
        return self["max_gap"]

    @property
    def num_gaps(self) -> List[Any]:
        return self["num_gaps"]

    @property
    def num_overlaps(self) -> List[Any]:
        return self["num_overlaps"]

    @property
    def pct_above_nhnm(self) -> List[Any]:
        return self["pct_above_nhnm"]

    @property
    def pct_below_nlnm(self) -> List[Any]:
        return self["pct_below_nlnm"]

    @property
    def percent_availability(self) -> List[Any]:
        return self["percent_availability"]

    @property
    def spikes(self) -> List[Any]:
        return self["spikes"]

    @property
    def pdf(self) -> List[Any]:
        return self["pdf"]


class GitLabAttachments(dict):
    '''
    Gitlab handler

    Params:
        list_of_attachments: List of dictionaries containing \
            GitLab attachment information
    '''

    def __init__(
        self,
        list_of_attachments: List[Any]
    ):
        self.list_of_attachments: List[Any] = list_of_attachments

    def get_attachments(self) -> Attachments:
        attachments: dict = {
            "failed_latencies": [],
            "latency_line_plot": [],
            "latency_log_plot": [],
            "timely_availability_plot": [],
            "timing_error": [],
            "timing_quality": [],
            "validation_results": [],
            "adc_count": [],
            "max_gap": [],
            "num_gaps": [],
            "num_overlaps": [],
            "pct_above_nhnm": [],
            "pct_below_nlnm": [],
            "percent_availability": [],
            "spikes": [],
            "pdf": []}
        for attachment in self.list_of_attachments:
            if "failed_latencies" in attachment["file_name"]:
                attachments["failed_latencies"].append(attachment)
            elif "latency_line_plot" in attachment["file_name"]:
                attachments["latency_line_plot"].append(attachment)
            elif "latency_log_plot" in attachment["file_name"]:
                attachments["latency_log_plot"].append(attachment)
            elif "timely_availability_plot" in attachment["file_name"]:
                attachments["timely_availability_plot"].append(attachment)
            elif "timing_error" in attachment["file_name"]:
                attachments["timing_error"].append(attachment)
            elif "timing_quality" in attachment["file_name"]:
                attachments["timing_quality"].append(attachment)
            elif "validation_results" in attachment["file_name"]:
                attachments["validation_results"].append(attachment)
            elif "adc_count" in attachment["file_name"]:
                attachments["adc_count"].append(attachment)
            elif "max_gap" in attachment["file_name"]:
                attachments["max_gap"].append(attachment)
            elif "num_gaps" in attachment["file_name"]:
                attachments["num_gaps"].append(attachment)
            elif "num_overlaps" in attachment["file_name"]:
                attachments["num_overlaps"].append(attachment)
            elif "pct_above_nhnm" in attachment["file_name"]:
                attachments["pct_above_nhnm"].append(attachment)
            elif "pct_below_nlnm" in attachment["file_name"]:
                attachments["pct_below_nlnm"].append(attachment)
            elif "percent_availability" in attachment["file_name"]:
                attachments["percent_availability"].append(attachment)
            elif "spikes" in attachment["file_name"]:
                attachments["spikes"].append(attachment)
            elif "pdf" in attachment["file_name"]:
                attachments["pdf"].append(attachment)
        return Attachments(attachments)
